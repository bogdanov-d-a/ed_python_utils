from typing import Optional
from . import file_tree_snapshot
from . import ibds_utils
from . import ibds_tablegen


def _multi_indexes(index_list: list[file_tree_snapshot.Index], complete_locations: set[int], name: Optional[str]=None) -> None:
    table = ibds_tablegen.indexes(index_list)
    complete_locations_list = sorted(list(complete_locations))

    diff_data: list[str] = []
    incomplete_location: list[str] = []

    table_items: list[tuple[str, list[Optional[file_tree_snapshot.FileInfo]]]] = ibds_utils.key_sorted_dict_items(table)
    for path, data in table_items:
        if (ibds_tablegen.get_same_hash(data) is None):
            diff_data.append(path)

        incomplete_count = 0
        for complete_location_index in complete_locations_list:
            if data[complete_location_index] is None:
                incomplete_count += 1

        if incomplete_count != 0:
            incomplete_location.append(path)

    print_lists: list[tuple[str, list[str]]] = [('Different data:', diff_data), ('Missing from complete location:', incomplete_location)]
    ibds_utils.print_lists(print_lists, name)


def multi_index_files(index_file_list: list[str], complete_locations: set[int], name: Optional[str]=None) -> None:
    index_list = list(map(lambda index_file: file_tree_snapshot.load_index(index_file), index_file_list))
    _multi_indexes(index_list, complete_locations, name)


def _multi_indexes_by_hash(index_list: list[file_tree_snapshot.Index], name: Optional[str]=None) -> None:
    table = ibds_tablegen.indexes_by_hash(index_list)

    unique_data: list[str] = []

    table_items: list[tuple[str, list[bool]]] = ibds_utils.key_sorted_dict_items(table)
    for hash_, data in table_items:
        true_count = data.count(True)
        if true_count == 0:
            raise Exception('_multi_indexes_by_hash true_count == 0')
        elif true_count == 1:
            unique_data.append(hash_)

    print_lists: list[tuple[str, list[str]]] = [('Unique data:', unique_data)]
    ibds_utils.print_lists(print_lists, name)


def multi_index_by_hash_files(index_file_list: list[str], name: Optional[str]=None) -> None:
    index_list = list(map(lambda index_file: file_tree_snapshot.load_index(index_file), index_file_list))
    _multi_indexes_by_hash(index_list, name)
