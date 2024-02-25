from ...utils.user_data import UserData


def update_data(user_data: UserData) -> None:
    from ...impl.update.data import update_data as impl
    from ...utils import user_interaction
    from ...utils import utils
    from concurrent.futures import ProcessPoolExecutor
    from multiprocessing import Manager

    storage_device = user_interaction.pick_storage_device(user_data.storage_devices)
    source_storage_devices = user_interaction.pick_storage_device_multi(user_data.storage_devices)

    aliases = list(utils.get_all_aliases_for_storage_device(user_data, storage_device))

    storage_path_cache: dict[str, str] = {}

    def data_sources_provider(collection_alias: str) -> list[tuple[str, str]]:
        collection_data = user_data.collection_dict[collection_alias]
        data_sources: list[tuple[str, str]] = []

        for source_storage_device in source_storage_devices:
            if source_storage_device in collection_data.storage_devices:
                collection_paths = utils.get_collection_paths(user_data, collection_alias, source_storage_device, storage_path_cache)
                data_sources.append((collection_paths.def_, collection_paths.get_data()))

        return data_sources

    manager = Manager()
    data_mutex = manager.Lock()

    with ProcessPoolExecutor(min(len(aliases), user_data.collection_processing_workers)) as executor:
        futures = list(map(
            lambda alias: executor.submit(
                impl,
                alias[1].def_,
                alias[1].get_data(),
                alias[1].get_data() + 'Recycle',
                data_sources_provider(alias[0]),
                data_mutex
            ),
            aliases
        ))

        for future in futures:
            future.result()
