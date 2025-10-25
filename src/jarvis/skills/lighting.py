"""Skill that connects natural language cues to lighting hardware actions."""
from __future__ import annotations

from jarvis.skills.base import Skill, SkillContext, SkillResult


class LightingSkill(Skill):
    name = "lighting"
    description = "Turn lights or other GPIO devices on and off."

    def __init__(self, device_name: str = "desk_lamp") -> None:
        self._device_name = device_name.lower()

    def can_handle(self, text: str) -> bool:
        lowered = text.lower()
        return self._device_name in lowered and (
            "turn on" in lowered or "turn off" in lowered
        )

    def handle(self, text: str, context: SkillContext) -> SkillResult:
        lowered = text.lower()
        if "turn on" in lowered:
            action = f"turn_on_{self._device_name}"
            response = f"Turning on the {self._device_name.replace('_', ' ')}."
        elif "turn off" in lowered:
            action = f"turn_off_{self._device_name}"
            response = f"Turning off the {self._device_name.replace('_', ' ')}."
        else:
            return SkillResult(handled=False)

        if not context.hardware.has_action(action):
            return SkillResult(
                handled=True,
                response=f"I do not have control of the {self._device_name} yet.",
            )

        context.hardware.execute(action)
        return SkillResult(handled=True, response=response)
