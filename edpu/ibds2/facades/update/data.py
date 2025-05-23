from ...utils import time
from ...utils.user_data import UserData


def update_data_helper(root_def_path: str, root_data_path: str, root_data_path_recycle: str, data_sources: list[tuple[str, str]], skip_descript_ion: bool) -> time.Collector:
    collector = time.Collector()

    with time.get_perf_counter_measure(collector, time.Key.WORKER1):
        from ...impl.update.data import update_data as impl
        impl(root_def_path, root_data_path, root_data_path_recycle, data_sources, skip_descript_ion, collector)
        return collector


def update_data(user_data: UserData) -> None:
    from ...utils import user_interaction

    storage_device = user_interaction.pick_storage_device(user_data.storage_devices)
    source_storage_devices = user_interaction.pick_storage_device_multi(user_data.storage_devices)

    def impl() -> None:
        from ...utils.mp_global import make_process_pool_executor
        from ...utils.utils import get_all_aliases_for_storage_device

        aliases = list(get_all_aliases_for_storage_device(user_data, storage_device))

        storage_path_cache: dict[str, str] = {}

        def data_sources_provider(collection_alias: str) -> list[tuple[str, str]]:
            collection_data = user_data.collection_dict[collection_alias]
            data_sources: list[tuple[str, str]] = []

            for source_storage_device in source_storage_devices:
                if source_storage_device in collection_data.storage_devices:
                    from ...utils.path import get_collection_paths

                    collection_paths = get_collection_paths(user_data, collection_alias, source_storage_device, storage_path_cache)
                    data_sources.append((collection_paths.def_, collection_paths.get_data()))

            return data_sources

        with make_process_pool_executor(min(len(aliases), user_data.collection_processing_workers)) as executor:
            from ...utils.path import RECYCLE_SUFFIX

            futures = list(map(
                lambda alias: executor.submit(
                    update_data_helper,
                    alias[1].def_,
                    alias[1].get_data(),
                    alias[1].get_data() + RECYCLE_SUFFIX,
                    data_sources_provider(alias[0]),
                    user_data.collection_dict[alias[0]].skip_descript_ion
                ),
                aliases
            ))

            for future in futures:
                collector_sum.merge(future.result())

    with time.CollectorPrinter() as collector_sum:
        with time.get_perf_counter_measure(collector_sum, time.Key.MAIN):
            impl()
