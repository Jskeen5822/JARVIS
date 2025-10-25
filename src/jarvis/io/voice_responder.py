"""Voice synthesis wrappers for local and cloud backends."""
from __future__ import annotations

import importlib
import importlib.util
from typing import Optional

from jarvis.config import SpeechOutputConfig


class VoiceResponder:
    """Convert assistant messages to audible speech."""

    def __init__(self, config: SpeechOutputConfig, *, text_fallback: bool = True) -> None:
        self._config = config
        self._text_fallback = text_fallback

        self._tts_engine = None
        if config.engine.lower() == "pyttsx3" and importlib.util.find_spec("pyttsx3"):
            pyttsx3 = importlib.import_module("pyttsx3")
            self._tts_engine = pyttsx3.init()
            if config.rate is not None:
                self._tts_engine.setProperty("rate", config.rate)
            if config.volume is not None:
                self._tts_engine.setProperty("volume", config.volume)
            if config.voice_id is not None:
                self._tts_engine.setProperty("voice", config.voice_id)

        self._elevenlabs = None
        if (
            config.engine.lower() == "elevenlabs"
            and config.elevenlabs_api_key
            and importlib.util.find_spec("elevenlabs")
        ):
            elevenlabs = importlib.import_module("elevenlabs")
            elevenlabs.set_api_key(config.elevenlabs_api_key)
            self._elevenlabs = elevenlabs

    def speak(self, message: str) -> None:
        message = message.strip()
        if not message:
            return

        if self._tts_engine:
            self._tts_engine.say(message)
            self._tts_engine.runAndWait()
            return

        if self._elevenlabs:
            voice = self._config.voice_id or "Rachel"
            self._elevenlabs.generate_and_play_audio(
                text=message,
                voice=voice,
                model="eleven_multilingual_v2",
            )
            return

        if self._text_fallback:
            print(f"Jarvis> {message}")
            return

        raise RuntimeError("No speech synthesis backend is available.")
