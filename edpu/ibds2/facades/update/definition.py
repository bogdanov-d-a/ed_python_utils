from ...utils import time
from ...utils.user_data import UserData


def update_definition_helper(root_data_path: str, root_def_path: str, skip_descript_ion: bool, skip_mtime: bool, debug: bool) -> time.Collector:
    collector = time.Collector()

    with time.get_perf_counter_measure(collector, time.Key.WORKER1):
        from ...impl.update.definition import update_definition as impl
        impl(root_data_path, root_def_path, skip_descript_ion, skip_mtime, debug, collector)
        return collector


def update_definition(user_data: UserData) -> None:
    from ...utils.user_interaction import pick_storage_device

    storage_device = pick_storage_device(user_data.storage_devices)

    def impl() -> None:
        from ...utils.mp_global import make_process_pool_executor
        from ...utils.utils import get_all_aliases_for_storage_device

        aliases = list(get_all_aliases_for_storage_device(user_data, storage_device))

        with make_process_pool_executor(min(len(aliases), user_data.collection_processing_workers)) as executor:
            futures = list(map(
                lambda alias: executor.submit(
                    update_definition_helper,
                    alias[1].get_data(),
                    alias[1].def_,
                    user_data.collection_dict[alias[0]].skip_descript_ion,
                    user_data.skip_mtime,
                    user_data.debug
                ),
                aliases
            ))

            for future in futures:
                collector_sum.merge(future.result())

    with time.CollectorPrinter() as collector_sum:
        with time.get_perf_counter_measure(collector_sum, time.Key.MAIN):
            impl()
