"""Hardware abstraction for Raspberry Pi, Arduino, or mock devices."""
from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import Callable, Dict, Optional

from jarvis.config import HardwareConfig


@dataclass(slots=True)
class HardwareAction:
    """Encapsulate a callable action and optional human-readable description."""

    handler: Callable[..., None]
    description: str = ""


class HardwareController:
    """Manage interactions with physical devices, with graceful fallbacks."""

    def __init__(self, config: HardwareConfig) -> None:
        self._config = config
        self._actions: Dict[str, HardwareAction] = {}
        self._platform = platform.system()

        self._gpio_ready = self._config.enable_gpio and self._platform != "Windows"
        if self._gpio_ready:
            try:
                import gpiozero  # type: ignore  # pragma: no cover

                self._gpio_lib = gpiozero
            except ImportError:
                self._gpio_ready = False
                self._gpio_lib = None
        else:
            self._gpio_lib = None

    def register_action(self, name: str, handler: Callable[..., None], *, description: str = "") -> None:
        self._actions[name.lower()] = HardwareAction(handler=handler, description=description)

    def has_action(self, name: str) -> bool:
        return name.lower() in self._actions

    def execute(self, name: str, **kwargs) -> None:
        action = self._actions.get(name.lower())
        if not action:
            raise KeyError(f"No hardware action registered under '{name}'.")
        action.handler(**kwargs)

    def summary(self) -> Dict[str, str]:
        return {name: action.description for name, action in self._actions.items()}

    # Example handlers -------------------------------------------------
    def attach_example_led(self, pin: int, name: str = "desk_lamp") -> None:
        if not self._gpio_ready:
            print("[hardware] GPIO not active; using simulated LED toggle.")
            self.register_action(
                f"turn_on_{name}",
                lambda: print(f"[hardware] {name} -> ON"),
                description=f"Simulated LED on pin {pin}",
            )
            self.register_action(
                f"turn_off_{name}",
                lambda: print(f"[hardware] {name} -> OFF"),
                description=f"Simulated LED on pin {pin}",
            )
            return

        led = self._gpio_lib.LED(pin)  # type: ignore[attr-defined]
        self.register_action(
            f"turn_on_{name}",
            led.on,
            description=f"LED on pin {pin}",
        )
        self.register_action(
            f"turn_off_{name}",
            led.off,
            description=f"LED on pin {pin}",
        )
