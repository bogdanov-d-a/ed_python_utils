from __future__ import annotations


class DriveData:
    def __init__(self: DriveData, name: str, path: str, size: int) -> None:
        self.name = name
        self.path = path
        self.size = size


    def print(self: DriveData) -> None:
        list_: list[tuple[str, str]] = [
            ('path', self.path),
            ('size', str(self.size)),
        ]

        for elem in list_:
            print(f'{self.name} {elem[0]}: {elem[1]}')
