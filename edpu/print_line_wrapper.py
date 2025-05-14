from __future__ import annotations
from typing import Callable


class PrintLineWrapper:
    def __init__(self: PrintLineWrapper, count: int=1) -> None:
        self._count = count

    def _print_lines(self: PrintLineWrapper) -> None:
        for _ in range(self._count):
            print()

    def __enter__(self: PrintLineWrapper) -> None:
        self._print_lines()

    def __exit__(self: PrintLineWrapper, exc_type, exc_value, exc_tb) -> None:
        self._print_lines()


def wrap_with_print_line(fn: Callable[[], None], count: int=1) -> Callable[[], None]:
    def result() -> None:
        with PrintLineWrapper(count):
            fn()

    return result
