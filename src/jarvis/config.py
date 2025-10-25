"""Project-wide configuration management for the JARVIS assistant."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

import os


@dataclass(slots=True)
class OpenAIConfig:
    """Runtime configuration for OpenAI-powered intelligence."""

    api_key: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    response_max_tokens: int = 500


@dataclass(slots=True)
class SpeechInputConfig:
    """Control microphone capture and transcription settings."""

    enable_microphone: bool = True
    use_whisper_api: bool = False
    device_index: Optional[int] = None
    phrase_time_limit: Optional[int] = None
    energy_threshold: Optional[int] = None


@dataclass(slots=True)
class SpeechOutputConfig:
    """Configure voice synthesis backends."""

    engine: str = "pyttsx3"
    rate: Optional[int] = None
    volume: Optional[float] = None
    voice_id: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None


@dataclass(slots=True)
class HardwareConfig:
    """Toggle Raspberry Pi / Arduino features based on the current host."""

    enable_gpio: bool = False
    gpio_board_mode: Optional[str] = None


@dataclass(slots=True)
class DashboardConfig:
    """Optional web dashboard settings."""

    enabled: bool = False
    host: str = "127.0.0.1"
    port: int = 5050


@dataclass(slots=True)
class Settings:
    """Top-level configuration container for the assistant."""

    root_dir: Path
    openai: OpenAIConfig
    speech_input: SpeechInputConfig
    speech_output: SpeechOutputConfig
    hardware: HardwareConfig
    dashboard: DashboardConfig


def load_settings(env_file: Optional[Path] = None) -> Settings:
    """Load configuration from environment variables and optional ``.env`` file."""

    if env_file is None:
        env_file = Path.cwd() / ".env"

    # loading is idempotent and safe if the file is missing
    load_dotenv(dotenv_path=env_file, override=False)

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise RuntimeError(
            "OPENAI_API_KEY is required. Create a .env file with the key or export it."
        )

    eleven_key = os.getenv("ELEVENLABS_API_KEY")

    return Settings(
        root_dir=Path.cwd(),
        openai=OpenAIConfig(
            api_key=openai_key,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
            response_max_tokens=int(os.getenv("OPENAI_RESPONSE_MAX_TOKENS", "500")),
        ),
        speech_input=SpeechInputConfig(
            enable_microphone=os.getenv("ENABLE_MICROPHONE", "true").lower()
            == "true",
            use_whisper_api=os.getenv("USE_WHISPER_API", "false").lower() == "true",
            device_index=_parse_optional_int(os.getenv("MIC_DEVICE_INDEX")),
            phrase_time_limit=_parse_optional_int(os.getenv("PHRASE_TIME_LIMIT")),
            energy_threshold=_parse_optional_int(os.getenv("ENERGY_THRESHOLD")),
        ),
        speech_output=SpeechOutputConfig(
            engine=os.getenv("VOICE_ENGINE", "pyttsx3"),
            rate=_parse_optional_int(os.getenv("VOICE_RATE")),
            volume=_parse_optional_float(os.getenv("VOICE_VOLUME")),
            voice_id=os.getenv("VOICE_ID"),
            elevenlabs_api_key=eleven_key,
        ),
        hardware=HardwareConfig(
            enable_gpio=os.getenv("ENABLE_GPIO", "false").lower() == "true",
            gpio_board_mode=os.getenv("GPIO_BOARD_MODE"),
        ),
        dashboard=DashboardConfig(
            enabled=os.getenv("DASHBOARD_ENABLED", "false").lower() == "true",
            host=os.getenv("DASHBOARD_HOST", "127.0.0.1"),
            port=int(os.getenv("DASHBOARD_PORT", "5050")),
        ),
    )


def _parse_optional_int(raw: Optional[str]) -> Optional[int]:
    if raw in (None, ""):
        return None
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Expected integer but received '{raw}'.") from exc


def _parse_optional_float(raw: Optional[str]) -> Optional[float]:
    if raw in (None, ""):
        return None
    try:
        return float(raw)
    except ValueError as exc:
        raise RuntimeError(f"Expected float but received '{raw}'.") from exc
