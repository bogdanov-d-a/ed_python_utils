import os
from .user_data import CollectionDict, COLLECTION_VALUE_LOCATIONS
from . import ibds_utils
from . import path_generator


def generate_target_file_list(collection_dict: CollectionDict) -> list[str]:
    list_: list[str] = []

    for name, data in collection_dict.items():
        for location in data[COLLECTION_VALUE_LOCATIONS]:
            list_.append(path_generator.gen_index_file_path(name, location.getStorageDevice(), None))
            list_.append(path_generator.gen_hashset_file_path(name, None, location.getStorageDevice()))
        list_.append(path_generator.gen_common_file_path(name, None))
        list_.append(path_generator.gen_hashset_file_path(name, None))

    return list_


def generate_actual_file_list(data_dir: str) -> list[str]:
    return os.listdir(data_dir)


def check_data_file_set(data_dir: str, collection_dict: CollectionDict) -> None:
    target = set(generate_target_file_list(collection_dict))
    actual = set(generate_actual_file_list(data_dir))

    print_lists: list[tuple[str, list[str]]] = [('Odd', sorted(actual - target)), ('Missing', sorted(target - actual))]
    ibds_utils.print_lists(print_lists)
