from ..utils import time
from typing import Callable, Optional


def _make_file_progress_printer(path_: str) -> Callable[[int], None]:
    from ...throttling import TimeBasedAggregator
    return TimeBasedAggregator.make_number_sum_printer(0.5, f'file_tree_scanner.scan {path_}')


def scan(root_path: str, skip_paths: list[str], collector: Optional[time.Collector]=None) -> list[list[str]]:
    from ...context_manager import DummyContextManager
    from ...file_tree_walker import walk, TYPE_DIR, TYPE_FILE
    from .utils import path_needs_skip

    with time.get_perf_counter_measure(collector, time.Key.WALK) if collector is not None else DummyContextManager():
        return walk(
            root_path,
            lambda type, path: type == TYPE_DIR or path_needs_skip(path, skip_paths),
            _make_file_progress_printer(root_path)
        )[TYPE_FILE]
