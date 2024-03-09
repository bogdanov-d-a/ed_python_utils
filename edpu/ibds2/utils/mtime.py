from . import time
from typing import Callable


def getmtime(path: str, progress_fn: Callable[[], None], collector: time.Collector) -> float:
    progress_fn()

    with time.get_perf_counter_measure(collector, time.Key.WORKER1_GETMTIME):
        from os.path import getmtime
        return getmtime(path)


def make_getmtime_progress_printer(path_: str) -> Callable[[], None]:
    return _make_count_printer('getmtime', path_)


def setmtime(path: str, time_: float, progress_fn: Callable[[], None], collector: time.Collector) -> None:
    progress_fn()

    with time.get_perf_counter_measure(collector, time.Key.WORKER1_SETMTIME):
        from os import utime
        utime(path, (time_, time_))


def make_setmtime_progress_printer(path_: str) -> Callable[[], None]:
    return _make_count_printer('setmtime', path_)


def _make_count_printer(annotation: str, path_: str) -> Callable[[], None]:
    from ...throttling import TimeBasedAggregator
    from .mp_global import print_lock

    return TimeBasedAggregator.make_count_printer(0.5, f'{annotation} {path_}', print_lock())
