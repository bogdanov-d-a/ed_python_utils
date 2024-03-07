from ..utils import time


def same_defs(path_a: str, path_b: str, collector: time.Collector) -> bool:
    from ..utils.mp_global import make_process_pool_executor

    with make_process_pool_executor(2) as executor:
        from ..utils.walk_helpers import walk_def
        results = list(executor.map(walk_def, [path_a, path_b]))

    collector.merge(results[0][1]).merge(results[1][1])

    return results[0][0] == results[1][0]
