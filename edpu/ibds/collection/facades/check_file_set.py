from ...utils.user_data import CollectionDict


def _generate_target_file_list(collection_dict: CollectionDict) -> list[str]:
    result: list[str] = []

    for name, data in collection_dict.items():
        from ...utils import path_generator
        from ...utils.user_data import COLLECTION_VALUE_LOCATIONS

        for location in data[COLLECTION_VALUE_LOCATIONS]:
            result.append(path_generator.gen_index_file_path(name, location.getStorageDevice(), None))
            result.append(path_generator.gen_hashset_file_path(name, None, location.getStorageDevice()))

        result.append(path_generator.gen_common_file_path(name, None))
        result.append(path_generator.gen_hashset_file_path(name, None))

    return result


def _generate_actual_file_list(data_dir: str) -> list[str]:
    from os import listdir
    return listdir(data_dir)


def check_data_file_set(data_dir: str, collection_dict: CollectionDict) -> None:
    from ...utils.utils import print_lists

    target = set(_generate_target_file_list(collection_dict))
    actual = set(_generate_actual_file_list(data_dir))

    print_lists([
        ('Odd', sorted(actual - target)),
        ('Missing', sorted(target - actual)),
    ])
