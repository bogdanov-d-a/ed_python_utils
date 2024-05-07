from __future__ import annotations
from .drive_data import DriveData
from typing import Optional


class DriveBlockData:
    def __init__(self: DriveBlockData, name: str, drive: DriveData, size: int, start: int=0, end: Optional[int]=None) -> None:
        self.name = name
        self.drive = drive
        self.size = size

        self.total = drive.size // self.size
        self.tail = drive.size % self.size

        self.start = start
        self.end = end if end is not None else self.total - 1

        if self.start >= self.total:
            raise Exception('self.start >= self.total')

        if self.end >= self.total:
            raise Exception('self.end >= self.total')

        self.count = self.end - self.start + 1


    def print(self: DriveBlockData) -> None:
        self.drive.print()

        list_: list[tuple[str, str]] = [
            ('size', str(self.size)),
            ('total', str(self.total)),
            ('tail', str(self.tail)),
            ('start', str(self.start)),
            ('end', str(self.end)),
            ('count', str(self.count)),
        ]

        for elem in list_:
            print(f'{self.drive.name} {self.name} {elem[0]}: {elem[1]}')
