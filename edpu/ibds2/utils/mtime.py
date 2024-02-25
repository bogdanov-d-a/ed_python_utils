from typing import Callable


def getmtime(path: str, progress_fn: Callable[[], None]) -> float:
    from os.path import getmtime

    progress_fn()
    return getmtime(path)


def make_getmtime_progress_printer(path_: str) -> Callable[[], None]:
    return _make_count_printer('getmtime', path_)


def setmtime(path: str, time: float, progress_fn: Callable[[], None]) -> None:
    from os import utime

    progress_fn()
    utime(path, (time, time))


def make_setmtime_progress_printer(path_: str) -> Callable[[], None]:
    return _make_count_printer('setmtime', path_)


def _make_count_printer(annotation: str, path_: str) -> Callable[[], None]:
    from edpu.throttling import TimeBasedAggregator
    return TimeBasedAggregator.make_count_printer(0.5, f'{annotation} {path_}')
