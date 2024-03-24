from __future__ import annotations
from .data import Data
from typing import Iterable


class _DayData:
    def __init__(self: _DayData) -> None:
        self.pcs = 0
        self.day_parts: list[str] = []


    def add(self: _DayData, pcs: int, day_part: str) -> None:
        self.pcs += pcs
        self.day_parts.append(day_part)


class DailyPcs:
    def __init__(self: DailyPcs, data: Data) -> None:
        self._data = data
        self._dict: dict[str, _DayData] = {}


    def add(self: DailyPcs, pcs: int, day: str, day_part: str) -> None:
        if day not in self._dict:
            self._dict[day] = _DayData()
        self._dict[day].add(pcs, day_part)


    def str(self: DailyPcs) -> Iterable[str]:
        for day, day_data in sorted(self._dict.items()):
            from .pcs_pretty_print import pcs_pretty_print
            yield f'{day} = {pcs_pretty_print(day_data.pcs, self._data)} - ({", ".join(day_data.day_parts)})'
