from __future__ import annotations
from time import perf_counter
from typing import Callable


class PerfCounterMeasure:
    def __init__(self: PerfCounterMeasure, handler: Callable[[float], None]) -> None:
        self._handler = handler

    def __enter__(self: PerfCounterMeasure):
        self._start = perf_counter()

    def __exit__(self: PerfCounterMeasure, exc_type, exc_value, exc_tb):
        self._handler(perf_counter() - self._start)
