from . import time
from .walkers import WalkDefResult


def walk_data(data_path: str, skip_descript_ion: bool) -> tuple[dict[str, set[str]], time.Collector]:
    collector = time.Collector()

    with time.get_perf_counter_measure(collector, time.Key.WORKER2):
        with time.get_perf_counter_measure(collector, time.Key.WORKER2_WALK_DATA_WITH_LOCK):
            from .mp_global import data_lock
            with data_lock():
                with time.get_perf_counter_measure(collector, time.Key.WORKER2_WALK_DATA):
                    from .walkers import walk_data as impl
                    return (impl(data_path, skip_descript_ion), collector)


def walk_def(def_path: str) -> tuple[WalkDefResult, time.Collector]:
    collector = time.Collector()

    with time.get_perf_counter_measure(collector, time.Key.WORKER2):
        with time.get_perf_counter_measure(collector, time.Key.WORKER2_WALK_DEF):
            from .walkers import walk_def as impl
            return (impl(def_path), collector)
