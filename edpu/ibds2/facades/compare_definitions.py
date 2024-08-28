from ..utils import time
from ..utils.user_data import UserData


def same_defs_helper(args: tuple[str, str]) -> tuple[bool, time.Collector]:
    collector = time.Collector()

    with time.get_perf_counter_measure(collector, time.Key.WORKER1):
        from ..impl.compare_definitions import same_defs
        path_a, path_b = args
        return (same_defs(path_a, path_b, collector), collector)


def compare_definitions(user_data: UserData) -> None:
    from ..utils.user_interaction import pick_storage_device
    from typing import Iterator

    storage_device_a = pick_storage_device(user_data.storage_devices, True)
    storage_device_b = pick_storage_device(user_data.storage_devices, True)

    def impl() -> Iterator[tuple[str, str]]:
        from ..utils.mp_global import make_process_pool_executor

        def get_def_paths(storage_device: str) -> dict[str, str]:
            from ..utils.utils import get_all_aliases_for_storage_device

            return {
                collection_alias: collection_paths.def_
                for collection_alias, collection_paths
                in get_all_aliases_for_storage_device(user_data, storage_device, find_data_path=False)
            }

        def_paths_a = get_def_paths(storage_device_a)
        def_paths_b = get_def_paths(storage_device_b)

        def_paths_list = list(map(
            lambda collection_alias: [def_paths_a[collection_alias], def_paths_b[collection_alias]],
            sorted(set(def_paths_a.keys()).intersection(set(def_paths_b.keys())))
        ))

        with make_process_pool_executor(min(len(def_paths_list), user_data.collection_processing_workers)) as executor:
            same_defs_list = list(executor.map(
                same_defs_helper,
                def_paths_list
            ))

        for def_paths, same_defs_tuple in zip(def_paths_list, same_defs_list):
            same_defs, collector = same_defs_tuple

            collector_sum.merge(collector)

            if not same_defs:
                yield (def_paths[0], def_paths[1])

    with time.CollectorPrinter() as collector_sum:
        with time.get_perf_counter_measure(collector_sum, time.Key.MAIN):
            result = list(impl())

    for path_a, path_b in result:
        user_data.diff_tool_handler(path_a, path_b)
