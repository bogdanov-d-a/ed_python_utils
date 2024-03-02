from ...utils.user_data import UserData


def update_definition(user_data: UserData) -> None:
    from ...utils.user_interaction import pick_storage_device
    from ...utils.utils import get_all_aliases_for_storage_device
    from concurrent.futures import ProcessPoolExecutor
    from multiprocessing import Manager

    storage_device = pick_storage_device(user_data.storage_devices)
    aliases = list(get_all_aliases_for_storage_device(user_data, storage_device))

    manager = Manager()
    data_mutex = manager.Lock()

    with ProcessPoolExecutor(min(len(aliases), user_data.collection_processing_workers)) as executor:
        from ...impl.update.definition import update_definition as impl

        futures = list(map(
            lambda alias: executor.submit(
                impl,
                alias[1].get_data(),
                alias[1].def_,
                user_data.skip_mtime,
                user_data.debug,
                data_mutex
            ),
            aliases
        ))

        for future in futures:
            future.result()
