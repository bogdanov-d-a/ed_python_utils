from __future__ import annotations
from typing import Any


class ValueStorage:
    def __init__(self: ValueStorage) -> None:
        self._values: dict[str, Any] = {}
        self._order: list[str] = []


    def add(self: ValueStorage, name: str, value: Any) -> None:
        if name in self._values:
            raise Exception('name in self._values')

        self._values[name] = value
        self._order.append(name)


    def get(self: ValueStorage, name: str) -> Any:
        return self._values[name]


    def print(self: ValueStorage) -> None:
        for name in self._order:
            value = self.get(name)

            if value is None:
                print()

            print(f'{name}: {str(value)}')


class ValueStoragePrinter:
    def __init__(self: ValueStoragePrinter) -> None:
        pass

    def __enter__(self: ValueStoragePrinter) -> ValueStorage:
        self._vs = ValueStorage()
        return self._vs

    def __exit__(self: ValueStoragePrinter, exc_type, exc_value, exc_tb) -> None:
        self._vs.print()
