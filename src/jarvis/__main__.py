"""Allow running ``python -m jarvis`` to start the assistant."""
from __future__ import annotations

from jarvis.core.assistant import JarvisAssistant
from jarvis.config import load_settings


def main() -> int:
    try:
        settings = load_settings()
    except Exception as exc:
        print(f"Failed to load configuration: {exc}")
        return 1

    JarvisAssistant(settings).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
