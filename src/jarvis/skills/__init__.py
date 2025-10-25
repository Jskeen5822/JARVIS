"""Skill system enabling custom voice commands."""

from jarvis.skills.base import Skill, SkillContext, SkillResult
from jarvis.skills.lighting import LightingSkill
from jarvis.skills.registry import SkillRegistry
from jarvis.skills.system_control import SystemControlSkill

__all__ = [
	"Skill",
	"SkillContext",
	"SkillResult",
	"LightingSkill",
	"SkillRegistry",
	"SystemControlSkill",
]
