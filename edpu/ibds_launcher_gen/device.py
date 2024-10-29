from __future__ import annotations


class Device:
    def __init__(self: Device, name: str, is_removable: bool, lock_name: str, disable_in_1: bool, use_in_2: bool) -> None:
        self.name = name
        self.is_removable = is_removable
        self.lock_name = lock_name
        self.disable_in_1 = disable_in_1
        self.use_in_2 = use_in_2
