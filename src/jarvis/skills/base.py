"""Base classes and utilities for defining assistant skills."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from jarvis.hardware.controller import HardwareController


@dataclass(slots=True)
class SkillContext:
    """Runtime dependencies passed to every skill invocation."""

    hardware: HardwareController


@dataclass(slots=True)
class SkillResult:
    """Outcome returned by a skill handler."""

    handled: bool
    response: Optional[str] = None


class Skill:
    """Abstract base class for custom skills."""

    name: str = "generic"
    description: str = ""

    def can_handle(self, text: str) -> bool:
        raise NotImplementedError

    def handle(self, text: str, context: SkillContext) -> SkillResult:
        raise NotImplementedError
