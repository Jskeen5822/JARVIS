"""Centralized logging configuration for the assistant."""
from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name or "jarvis")
