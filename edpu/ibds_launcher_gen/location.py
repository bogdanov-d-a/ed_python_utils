from __future__ import annotations


class Location:
    def __init__(self: Location, storage_device: str, path: str, is_complete: bool) -> None:
        self.storage_device = storage_device
        self.path = path
        self.is_complete = is_complete
