from __future__ import annotations
from .data import Data


class Stats:
    def __init__(self: Stats, data: Data) -> None:
        self._data = data

        self.stock = 0
        self.consumed = 0
        self.lost = 0


    def str(self: Stats) -> str:
        from .pcs_pretty_print import pcs_pretty_print

        return ', '.join(map(
            lambda e: f'{e[0]} = {pcs_pretty_print(e[1], self._data)}',
            [
                ('stock', self.stock),
                ('consumed', self.consumed),
                ('lost', self.lost),
            ]
        ))
