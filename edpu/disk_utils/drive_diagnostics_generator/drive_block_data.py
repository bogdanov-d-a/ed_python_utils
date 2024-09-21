from __future__ import annotations
from typing import Optional


class DriveBlockData:
    def __init__(self: DriveBlockData, name: str, size: str, start: Optional[str]=None, end: Optional[str]=None) -> None:
        self.name = name
        self.size = size
        self.start = start
        self.end = end
