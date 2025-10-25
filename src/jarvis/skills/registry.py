"""Registry that stores and dispatches skill handlers."""
from __future__ import annotations

from typing import Iterable, List, Optional

from jarvis.skills.base import Skill, SkillContext, SkillResult


class SkillRegistry:
    """Simple in-memory registry for skill discovery and execution."""

    def __init__(self, skills: Optional[Iterable[Skill]] = None) -> None:
        self._skills: List[Skill] = list(skills or [])

    def register(self, skill: Skill) -> None:
        self._skills.append(skill)

    def extend(self, skills: Iterable[Skill]) -> None:
        for skill in skills:
            self.register(skill)

    def handle(self, text: str, context: SkillContext) -> Optional[SkillResult]:
        for skill in self._skills:
            if skill.can_handle(text):
                result = skill.handle(text, context)
                if result.handled:
                    return result
        return None

    def names(self) -> List[str]:
        return [skill.name for skill in self._skills]
