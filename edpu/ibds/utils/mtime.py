from . import time
from typing import Callable


def getmtime(path: str, progress_fn: Callable[[], None], collector: time.Collector) -> float:
    progress_fn()

    with time.get_perf_counter_measure(collector, time.Key.GETMTIME):
        from os.path import getmtime
        return getmtime(path)


def make_getmtime_progress_printer(path_: str) -> Callable[[], None]:
    return _make_count_printer('getmtime', path_)


def _make_count_printer(annotation: str, path_: str) -> Callable[[], None]:
    from ...throttling import TimeBasedAggregator
    return TimeBasedAggregator.make_count_printer(0.5, f'{annotation} {path_}')
