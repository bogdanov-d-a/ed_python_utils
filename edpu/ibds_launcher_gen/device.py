from __future__ import annotations


class Device:
    def __init__(self: Device, name: str, is_removable: bool, use_in_2: bool) -> None:
        self.name = name
        self.is_removable = is_removable
        self.use_in_2 = use_in_2
