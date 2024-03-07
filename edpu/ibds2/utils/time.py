from __future__ import annotations
from edpu.perf_counter_measure import PerfCounterMeasure
from enum import Enum, auto


class Key(Enum):
    MAIN = auto()
    WORKER1 = auto()
    WORKER1_GETMTIME = auto()
    WORKER1_SETMTIME = auto()
    WORKER2 = auto()
    WORKER2_WALK_DEF = auto()
    WORKER2_WALK_DATA = auto()
    WORKER2_WALK_DATA_WITH_LOCK = auto()


class Collector:
    def __init__(self: Collector) -> None:
        self._data: dict[Key, float] = {}

    def add(self: Collector, key: Key, time: float) -> Collector:
        if key not in self._data:
            self._data[key] = 0
        self._data[key] += time
        return self

    def merge(self: Collector, other: Collector) -> Collector:
        for key, time in other._data.items():
            self.add(key, time)
        return self

    def print(self: Collector) -> None:
        for key, time in self._data.items():
            print(f'{key} - {time}')


class CollectorPrinter:
    def __init__(self: CollectorPrinter) -> None:
        self._collector = Collector()

    def __enter__(self: CollectorPrinter) -> Collector:
        return self._collector

    def __exit__(self: CollectorPrinter, exc_type, exc_value, exc_tb):
        print('CollectorPrinter')
        self._collector.print()


def get_perf_counter_measure(collector: Collector, key: Key) -> PerfCounterMeasure:
    def handler(time: float) -> None:
        collector.add(key, time)

    return PerfCounterMeasure(handler)
