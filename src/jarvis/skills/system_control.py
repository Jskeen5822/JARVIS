"""Skill for performing common desktop automation tasks."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from jarvis.skills.base import Skill, SkillContext, SkillResult


class SystemControlSkill(Skill):
    name = "system_control"
    description = "Launch desktop applications and perform OS commands."

    def can_handle(self, text: str) -> bool:
        lowered = text.lower()
        return any(keyword in lowered for keyword in ("open", "launch", "start"))

    def handle(self, text: str, context: SkillContext) -> SkillResult:
        lowered = text.lower()
        if "visual studio code" in lowered or "vs code" in lowered:
            self._launch_vscode()
            return SkillResult(handled=True, response="Opening Visual Studio Code.")

        if "terminal" in lowered:
            self._launch_terminal()
            return SkillResult(handled=True, response="Terminal is on the way.")

        return SkillResult(handled=False)

    def _launch_vscode(self) -> None:
        command = self._detect_vscode_command()
        subprocess.Popen(command, shell=True)

    def _launch_terminal(self) -> None:
        if os.name == "nt":
            subprocess.Popen("start powershell", shell=True)
        else:
            subprocess.Popen(["gnome-terminal"])  # basic fallback

    def _detect_vscode_command(self) -> str:
        if os.name == "nt":
            return "code"

        candidates = ["code", "/usr/bin/code", "/snap/bin/code"]
        for candidate in candidates:
            if Path(candidate).exists():
                return candidate
        return "code"
