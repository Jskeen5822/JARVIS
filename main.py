"""Entry point for the JARVIS assistant."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from jarvis.config import load_settings
from jarvis.core.assistant import JarvisAssistant


def main() -> int:
    try:
        settings = load_settings()
    except Exception as exc:
        print(f"Failed to load configuration: {exc}")
        return 1

    assistant = JarvisAssistant(settings)
    assistant.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
