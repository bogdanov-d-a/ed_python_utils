from .file_tree_snapshot import Index
from typing import Optional


def _multi_indexes(index_list: list[Index], complete_locations: set[int], name: Optional[str]=None) -> None:
    from ..utils.utils import key_sorted_dict_items, print_lists
    from .file_tree_snapshot import FileInfo
    from .tablegen import indexes, get_same_hash

    table = indexes(index_list)
    complete_locations_list = sorted(list(complete_locations))

    diff_data: list[str] = []
    incomplete_location: list[str] = []

    table_items: list[tuple[str, list[Optional[FileInfo]]]] = key_sorted_dict_items(table)

    for path, data in table_items:
        if get_same_hash(data) is None:
            diff_data.append(path)

        incomplete_count = 0

        for complete_location_index in complete_locations_list:
            if data[complete_location_index] is None:
                incomplete_count += 1

        if incomplete_count != 0:
            incomplete_location.append(path)

    print_lists(
        [
            ('Different data:', diff_data),
            ('Missing from complete location:', incomplete_location),
        ],
        name
    )


def multi_index_files(index_file_list: list[str], complete_locations: set[int], name: Optional[str]=None) -> None:
    from .file_tree_snapshot import load_index

    _multi_indexes(
        list(map(load_index, index_file_list)),
        complete_locations,
        name
    )


def _multi_indexes_by_hash(index_list: list[Index], name: Optional[str]=None) -> None:
    from ..utils.utils import key_sorted_dict_items, print_lists
    from .tablegen import indexes_by_hash

    table = indexes_by_hash(index_list)
    unique_data: list[str] = []
    table_items: list[tuple[str, list[bool]]] = key_sorted_dict_items(table)

    for hash_, data in table_items:
        true_count = data.count(True)

        if true_count == 0:
            raise Exception('_multi_indexes_by_hash true_count == 0')

        elif true_count == 1:
            unique_data.append(hash_)

    print_lists(
        [
            ('Unique data:', unique_data),
        ],
        name
    )


def multi_index_by_hash_files(index_file_list: list[str], name: Optional[str]=None) -> None:
    from .file_tree_snapshot import load_index
    _multi_indexes_by_hash(list(map(load_index, index_file_list)), name)
