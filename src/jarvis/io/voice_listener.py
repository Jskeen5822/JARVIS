"""Microphone listener that supports SpeechRecognition and Whisper API."""
from __future__ import annotations

import contextlib
import importlib
import importlib.util
import tempfile
from pathlib import Path
from typing import Any, Optional

from jarvis.config import SpeechInputConfig
from jarvis.integrations.openai_client import OpenAIClient

sr = None
if importlib.util.find_spec("speech_recognition"):
    sr = importlib.import_module("speech_recognition")


class VoiceListener:
    """Capture microphone input and convert it to text."""

    def __init__(
        self,
        config: SpeechInputConfig,
        *,
        openai_client: Optional[OpenAIClient] = None,
        fallback_to_text: bool = True,
    ) -> None:
        self._config = config
        self._openai_client = openai_client
        self._fallback_to_text = fallback_to_text
        self._recognizer = sr.Recognizer() if sr else None

        if self._recognizer and self._config.energy_threshold:
            self._recognizer.energy_threshold = self._config.energy_threshold

    def listen(self, *, prompt: str = "") -> str:
        """Record audio once and return the recognized transcript."""

        microphone_ready = (
            self._config.enable_microphone
            and self._recognizer
            and sr
            and sr.Microphone.list_microphone_names()
        )

        if microphone_ready:
            return self._listen_with_microphone(prompt=prompt)

        if self._fallback_to_text:
            displayed_prompt = prompt or "You> "
            return input(displayed_prompt)
        raise RuntimeError(
            "SpeechRecognition microphone not available and text fallback disabled."
        )

    # ------------------------------------------------------------------
    def _listen_with_microphone(self, *, prompt: str) -> str:
        assert self._recognizer and sr  # guarded by listen

        microphone_kwargs = {}
        if self._config.device_index is not None:
            microphone_kwargs["device_index"] = self._config.device_index

        with contextlib.ExitStack() as stack:
            microphone = stack.enter_context(sr.Microphone(**microphone_kwargs))
            print(prompt or "Listening... (speak now)")
            audio = self._recognizer.listen(
                microphone,
                timeout=None,
                phrase_time_limit=self._config.phrase_time_limit,
            )

        if self._config.use_whisper_api:
            if not self._openai_client:
                raise RuntimeError("Whisper API requested but OpenAI client is missing.")
            return self._transcribe_with_whisper(audio)

        try:
            return self._recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            raise RuntimeError(f"SpeechRecognition request failed: {exc}") from exc

    def _transcribe_with_whisper(self, audio: Any) -> str:
        assert self._openai_client
        wav_bytes = audio.get_wav_data(convert_rate=16000)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
            handle.write(wav_bytes)
            tmp_path = Path(handle.name)
        try:
            return self._openai_client.transcribe_audio(tmp_path)
        finally:
            with contextlib.suppress(FileNotFoundError):
                tmp_path.unlink()
