from ..utils.user_data import UserData


def same_defs_helper(args: tuple[str, str]) -> bool:
    from ..impl.compare_definitions import same_defs

    path_a, path_b = args
    return same_defs(path_a, path_b)


def compare_definitions(user_data: UserData) -> None:
    from ..utils import utils
    from ..utils.user_interaction import pick_storage_device
    from concurrent.futures import ProcessPoolExecutor

    def get_def_paths(storage_device: str) -> dict[str, str]:
        return {
            collection_alias: collection_paths.def_
            for collection_alias, collection_paths
            in utils.get_all_aliases_for_storage_device(user_data, storage_device, find_data_path=False)
        }

    def_paths_a = get_def_paths(pick_storage_device(user_data.storage_devices))
    def_paths_b = get_def_paths(pick_storage_device(user_data.storage_devices))

    def_paths_list = list(map(
        lambda collection_alias: [def_paths_a[collection_alias], def_paths_b[collection_alias]],
        sorted(set(def_paths_a.keys()).intersection(set(def_paths_b.keys())))
    ))

    with ProcessPoolExecutor(min(len(def_paths_list), user_data.collection_processing_workers)) as executor:
        same_defs_list = list(executor.map(
            same_defs_helper,
            def_paths_list
        ))

    for def_paths, same_defs in zip(def_paths_list, same_defs_list):
        if not same_defs:
            user_data.diff_tool_handler(def_paths[0], def_paths[1])
