"""Bridge pattern.

Reference: https://refactoring.guru/design-patterns/bridge

Intent
------
Split a large class or a set of closely related classes into two separate
hierarchies — abstraction and implementation — which can be developed
independently of each other.

Example
-------
Remote controls (abstraction) and devices (implementation) form two independent
hierarchies. A basic remote works with any device via a common Device interface.
An AdvancedRemote extends it with a mute shortcut — without touching any device
code. New devices (Tv, Radio) can be added without changing any remote code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# --- Implementation ----------------------------------------------------------
# Declares the low-level operations that all concrete devices must provide.
# The abstraction (remote) only ever calls these primitives.

class Device(ABC):
    @abstractmethod
    def is_enabled(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def enable(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def disable(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_volume(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_volume(self, percent: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_channel(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_channel(self, channel: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def status(self) -> str:
        raise NotImplementedError


# --- Concrete Implementations ------------------------------------------------

class Tv(Device):
    def __init__(self) -> None:
        self._on = False
        self._volume = 30
        self._channel = 1

    def is_enabled(self) -> bool:
        return self._on

    def enable(self) -> None:
        self._on = True

    def disable(self) -> None:
        self._on = False

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int) -> None:
        self._channel = channel

    def status(self) -> str:
        state = "ON" if self._on else "OFF"
        return f"TV      | {state} | vol={self._volume:3d} | ch={self._channel}"


class Radio(Device):
    def __init__(self) -> None:
        self._on = False
        self._volume = 50
        self._channel = 1

    def is_enabled(self) -> bool:
        return self._on

    def enable(self) -> None:
        self._on = True

    def disable(self) -> None:
        self._on = False

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int) -> None:
        self._channel = channel

    def status(self) -> str:
        state = "ON" if self._on else "OFF"
        return f"Radio   | {state} | vol={self._volume:3d} | ch={self._channel}"


# --- Abstraction -------------------------------------------------------------
# High-level control logic. Holds a reference to a Device and delegates all
# primitive work to it. Knows nothing about Tv or Radio specifically.

class RemoteControl:
    def __init__(self, device: Device) -> None:
        self._device = device

    def toggle_power(self) -> None:
        if self._device.is_enabled():
            self._device.disable()
        else:
            self._device.enable()

    def volume_down(self) -> None:
        self._device.set_volume(self._device.get_volume() - 10)

    def volume_up(self) -> None:
        self._device.set_volume(self._device.get_volume() + 10)

    def channel_down(self) -> None:
        self._device.set_channel(self._device.get_channel() - 1)

    def channel_up(self) -> None:
        self._device.set_channel(self._device.get_channel() + 1)


# --- Refined Abstraction -----------------------------------------------------
# Extends RemoteControl with an extra feature (mute) without touching any
# device code. The two hierarchies grow independently.

class AdvancedRemoteControl(RemoteControl):
    def mute(self) -> None:
        self._device.set_volume(0)


# --- Client ------------------------------------------------------------------

def client_code(remote: RemoteControl, label: str) -> None:
    print(f"--- {label} ---")
    remote.toggle_power()                   # turn on
    print(remote._device.status())
    remote.volume_up()
    remote.volume_up()
    print(remote._device.status())
    remote.channel_up()
    remote.channel_up()
    print(remote._device.status())
    if isinstance(remote, AdvancedRemoteControl):
        remote.mute()
        print(remote._device.status())
    remote.toggle_power()                   # turn off
    print(remote._device.status())


if __name__ == "__main__":
    client_code(RemoteControl(Tv()), "Basic remote + TV")
    print()
    client_code(AdvancedRemoteControl(Radio()), "Advanced remote + Radio")
