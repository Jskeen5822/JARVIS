"""Primary event loop that powers the JARVIS assistant experience."""
from __future__ import annotations

from typing import List

from jarvis.config import Settings
from jarvis.hardware.controller import HardwareController
from jarvis.integrations.openai_client import OpenAIClient
from jarvis.io.voice_listener import VoiceListener
from jarvis.io.voice_responder import VoiceResponder
from jarvis.skills.base import SkillContext
from jarvis.skills.lighting import LightingSkill
from jarvis.skills.registry import SkillRegistry
from jarvis.skills.system_control import SystemControlSkill
from jarvis.utils.logger import configure_logging, get_logger

_EXIT_KEYWORDS: List[str] = ["quit", "exit", "shutdown", "stop listening"]
_SYSTEM_PROMPT = (
    "You are JARVIS, an affable AI assistant that controls software and hardware at the "
    "user's desk. Keep answers short and take actions when skills are available."
)


class JarvisAssistant:
    """Coordinates audio IO, intelligent responses, and skill routing."""

    def __init__(self, settings: Settings) -> None:
        configure_logging()
        self._log = get_logger("jarvis.assistant")

        self._settings = settings
        self._openai = OpenAIClient(settings.openai)
        self._hardware = HardwareController(settings.hardware)
        self._listener = VoiceListener(
            settings.speech_input,
            openai_client=self._openai if settings.speech_input.use_whisper_api else None,
            fallback_to_text=True,
        )
        self._responder = VoiceResponder(settings.speech_output)

        if not settings.speech_input.enable_microphone:
            self._log.info("Microphone disabled; using terminal text input mode.")

        self._register_default_hardware()
        self._skills = self._build_skill_registry()
        self._context = SkillContext(hardware=self._hardware)

    def run(self) -> None:
        self._log.info("Jarvis assistant is alive. Say something!")
        while True:
            try:
                user_text = self._listener.listen(prompt="You> ")
            except KeyboardInterrupt:
                self._log.info("Interrupted by user. Shutting down.")
                break
            except Exception as exc:
                self._log.exception("Failed to capture audio: %s", exc)
                self._responder.speak("I could not hear you. Please try again.")
                continue

            cleaned = user_text.strip()
            if not cleaned:
                continue

            if cleaned.lower() in _EXIT_KEYWORDS:
                self._responder.speak("Goodbye!")
                break

            handled = self._try_handle_with_skills(cleaned)
            if handled:
                continue

            self._fallback_to_chatgpt(cleaned)

    # ------------------------------------------------------------------
    def _try_handle_with_skills(self, text: str) -> bool:
        skill_result = self._skills.handle(text, self._context)
        if not skill_result:
            return False
        if skill_result.response:
            self._responder.speak(skill_result.response)
        return skill_result.handled

    def _fallback_to_chatgpt(self, text: str) -> None:
        try:
            response = self._openai.generate_response(
                text,
                system_prompt=_SYSTEM_PROMPT,
            )
        except Exception as exc:
            self._log.exception("OpenAI request failed: %s", exc)
            self._responder.speak("I ran into an issue reaching OpenAI.")
            return
        self._responder.speak(response)

    def _register_default_hardware(self) -> None:
        # Register a simulated LED so users can observe the flow before wiring hardware.
        self._hardware.attach_example_led(pin=17, name="desk_lamp")

    def _build_skill_registry(self) -> SkillRegistry:
        registry = SkillRegistry(
            skills=[
                SystemControlSkill(),
                LightingSkill(device_name="desk_lamp"),
            ]
        )
        self._log.debug("Loaded skills: %s", ", ".join(registry.names()))
        return registry
