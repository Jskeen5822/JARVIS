"""Wrapper around the OpenAI SDK for text and audio tasks."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from openai import OpenAI

try:  # pragma: no cover - import path differs by SDK version
    from openai import OpenAIError  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    from openai.error import OpenAIError  # type: ignore[no-redef]

from jarvis.config import OpenAIConfig


class OpenAIClient:
    """Thin convenience layer to centralize OpenAI interactions."""

    def __init__(self, config: OpenAIConfig) -> None:
        self._config = config
        self._client = OpenAI(api_key=config.api_key)

    def generate_response(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[Iterable[dict]] = None,
    ) -> str:
        """Request a chat completion from the configured model."""

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})

        try:
            response = self._client.chat.completions.create(
                model=self._config.model,
                messages=messages,
                temperature=self._config.temperature,
                max_tokens=self._config.response_max_tokens,
            )
        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI chat completion failed: {exc}") from exc

        if not response.choices:
            raise RuntimeError("OpenAI returned no completion choices.")

        message = response.choices[0].message
        if not message or not message.content:
            raise RuntimeError("OpenAI completion contained no message content.")
        return message.content

    def transcribe_audio(
        self, audio_path: Path, *, model: str = "whisper-1"
    ) -> str:
        """Send an audio file to the Whisper API and return the transcript."""

        try:
            with audio_path.open("rb") as handle:
                transcript = self._client.audio.transcriptions.create(
                    model=model,
                    file=handle,
                )
        except OpenAIError as exc:
            raise RuntimeError(f"Audio transcription failed: {exc}") from exc

        text = getattr(transcript, "text", None) or getattr(transcript, "data", None)
        if isinstance(text, str):
            return text
        if isinstance(text, dict) and "text" in text:
            return str(text["text"])
        raise RuntimeError("Unexpected response format from Whisper API.")
