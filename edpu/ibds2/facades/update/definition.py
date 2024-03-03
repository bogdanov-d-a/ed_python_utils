from ...utils import time
from ...utils.user_data import UserData
from threading import Lock


def update_definition_helper(root_data_path: str, root_def_path: str, skip_mtime: bool, debug: bool, data_mutex: Lock) -> time.Collector:
    collector = time.Collector()

    with time.get_perf_counter_measure(collector, time.Key.WORKER1):
        from ...impl.update.definition import update_definition as impl
        impl(root_data_path, root_def_path, skip_mtime, debug, data_mutex, collector)
        return collector


def update_definition(user_data: UserData) -> None:
    from ...utils.user_interaction import pick_storage_device
    from ...utils.utils import get_all_aliases_for_storage_device
    from concurrent.futures import ProcessPoolExecutor
    from multiprocessing import Manager

    storage_device = pick_storage_device(user_data.storage_devices)

    def impl() -> None:
        aliases = list(get_all_aliases_for_storage_device(user_data, storage_device))

        manager = Manager()
        data_mutex = manager.Lock()

        with ProcessPoolExecutor(min(len(aliases), user_data.collection_processing_workers)) as executor:
            futures = list(map(
                lambda alias: executor.submit(
                    update_definition_helper,
                    alias[1].get_data(),
                    alias[1].def_,
                    user_data.skip_mtime,
                    user_data.debug,
                    data_mutex
                ),
                aliases
            ))

            for future in futures:
                collector_sum.merge(future.result())

    with time.CollectorPrinter() as collector_sum:
        with time.get_perf_counter_measure(collector_sum, time.Key.MAIN):
            impl()
