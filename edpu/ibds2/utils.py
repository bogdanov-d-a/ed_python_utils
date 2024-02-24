from __future__ import annotations
from io import BufferedReader, BufferedWriter, TextIOWrapper
import os
import shutil
from typing import Callable, Iterator, Optional
from .constants import *
from edpu import file_hashing
from edpu import user_interaction
from edpu import storage_finder


def strip_crlf(str_: str) -> str:
    return str_.rstrip('\n').rstrip('\r')


def type_to_prefix(type_: str) -> str:
    if type_ == TYPE_DIR:
        return 'd'
    elif type_ == TYPE_FILE:
        return 'f'
    else:
        raise Exception()


def prefix_to_type(prefix: str) -> str:
    if prefix == 'd':
        return TYPE_DIR
    elif prefix == 'f':
        return TYPE_FILE
    else:
        raise Exception()


def def_path_to_data_path(def_path: list[str]) -> tuple[str, list[str]]:
    type_ = prefix_to_type(def_path[-1][0])
    data_path = list(map(lambda a: a[1:], def_path[:-1])) + [def_path[-1][1:]]
    return type_, data_path


def data_path_to_def_path(path_: list[str], type_: str) -> list[str]:
    return list(map(lambda a: '_' + a, path_[:-1])) + [type_to_prefix(type_) + path_[-1]]


def hash_file(path: str) -> str:
    print('Calculating hash for ' + path)
    return file_hashing.sha512_file(path)


def getmtime(path: str, progress_fn: Callable[[], None]) -> float:
    progress_fn()
    return os.path.getmtime(path)


def make_getmtime_progress_printer(path_: str) -> Callable[[], None]:
    return make_count_printer('getmtime', path_)


def setmtime(path: str, time: float, progress_fn: Callable[[], None]) -> None:
    progress_fn()
    os.utime(path, (time, time))


def make_setmtime_progress_printer(path_: str) -> Callable[[], None]:
    return make_count_printer('setmtime', path_)


def make_count_printer(annotation: str, path_: str) -> Callable[[], None]:
    from edpu.throttling import TimeBasedAggregator
    return TimeBasedAggregator.make_count_printer(0.5, f'{annotation} {path_}')


def path_to_root(path: list[str], root: str) -> str:
    return os.path.join(root, os.sep.join(path))


def makedirs_helper(path: list[str], root: str, is_file: bool) -> None:
    if is_file:
        if len(path) <= 1:
            return
        path = path[:-1]

    os.makedirs(path_to_root(path, root), exist_ok=True)


def path_to_key(path: list[str]) -> str:
    return INDEX_PATH_SEPARATOR.join(path)


def key_to_path(key: str) -> list[str]:
    return key.split(INDEX_PATH_SEPARATOR)


def intersection_handler(main_list: set[str], aux_list: set[str], use_intersection: bool, action: Callable[[list[str]], None]) -> None:
    for main_content in main_list:
        if (main_content in aux_list) == use_intersection:
            action(key_to_path(main_content))


def get_storage_device_list(storage_devices: StorageDevices) -> list[str]:
    storage_device_list: list[str] = []

    for device_name, device_data in storage_devices.items():
        if device_data[IS_SCAN_AVAILABLE_KEY]:
            storage_device_list.append(device_name)

    return storage_device_list


def pick_storage_device(storage_devices: StorageDevices) -> str:
    storage_device_list = get_storage_device_list(storage_devices)
    storage_device_list_cmds: list[tuple[str, str]] = user_interaction.generate_cmds(storage_device_list)
    storage_device_list_cmds_dict: dict[str, str] = user_interaction.list_to_dict(storage_device_list_cmds)

    str_options = user_interaction.pick_str_option_multi('Choose storage device', storage_device_list_cmds, lambda set_: 'only one device allowed' if len(set_) != 1 else None)
    return storage_device_list_cmds_dict[str_options[0]]


def pick_storage_device_multi(storage_devices: StorageDevices) -> list[str]:
    storage_device_list = get_storage_device_list(storage_devices)
    storage_device_list_cmds: list[tuple[str, str]] = user_interaction.generate_cmds(storage_device_list)
    storage_device_list_cmds_dict: dict[str, str] = user_interaction.list_to_dict(storage_device_list_cmds)

    result: list[str] = []

    for picked_cmd in user_interaction.pick_str_option_multi('Choose storage devices', storage_device_list_cmds):
        result.append(storage_device_list_cmds_dict[picked_cmd])

    return result


def get_bundle_aliases(user_data: UserData) -> list[str]:
    set_: set[str] = set()

    for collection_data in user_data[COLLECTION_DICT_KEY].values():
        set_ |= set(collection_data[BUNDLE_ALIASES_KEY].keys())

    return sorted(set_)


def pick_bundle_alias(bundle_aliases: list[str]) -> str:
    return bundle_aliases[user_interaction.pick_option('Choose bundle alias', bundle_aliases)]


def pick_bundle_slice_alias(bundle_slices: dict[str, str]) -> str:
    bundle_slices_list = list(sorted(bundle_slices.keys()))
    return bundle_slices_list[user_interaction.pick_option('Choose bundle slice alias', bundle_slices_list)]


def pick_collection_alias(collection_dict: CollectionDict) -> str:
    collection_aliases = list(sorted(collection_dict.keys()))
    return collection_aliases[user_interaction.pick_option('Choose collection alias', collection_aliases)]


def get_storage_path(storage_device_name: str, storage_path_cache: dict[str, str]) -> str:
    storage_path = storage_path_cache.get(storage_device_name)

    if storage_path is not None:
        return storage_path

    storage_path = storage_finder.keep_getting_storage_path(storage_device_name)
    storage_path_cache[storage_device_name] = storage_path
    return storage_path


class GetCollectionPathsResult:
    def __init__(self: GetCollectionPathsResult, def_: str, data: Optional[str]) -> None:
        self.def_ = def_
        self._data = data

    def get_data(self: GetCollectionPathsResult) -> str:
        if self._data is None:
            raise Exception()
        return self._data


def get_collection_paths(user_data: UserData, collection_alias: str, storage_device_name: str, storage_path_cache: dict[str, str], find_data_path: bool=True) -> GetCollectionPathsResult:
    collection_dict: CollectionDict = user_data[COLLECTION_DICT_KEY]
    storage_devices: StorageDevices = user_data[STORAGE_DEVICES_KEY]
    data_path: str = user_data[DATA_PATH_KEY]

    collection_data = collection_dict[collection_alias]
    collection_storage_devices: CollectionStorageDevices = collection_data[STORAGE_DEVICES_KEY]
    collection_storage_device_data = collection_storage_devices[storage_device_name]
    storage_device = storage_devices[storage_device_name]

    if find_data_path:
        abs_data_path = collection_storage_device_data
        if storage_device[IS_REMOVABLE_KEY]:
            abs_data_path = get_storage_path(storage_device_name, storage_path_cache) + abs_data_path
    else:
        abs_data_path = None

    abs_def_path = os.path.join(data_path, collection_alias, storage_device_name)

    return GetCollectionPathsResult(abs_def_path, abs_data_path)


def get_bundle_file_name(bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    return bundle_alias + '-' + collection_alias + '-' + bundle_slice_alias


def get_bundle_file_path(user_data: UserData, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    return os.path.join(user_data[BUNDLES_PATH_KEY], get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias))


def get_bundle_snap_path(user_data: UserData, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> str:
    return os.path.join(user_data[BUNDLE_SNAPS_PATH_KEY], get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias) + '.txt')


def get_all_aliases_for_storage_device(user_data: UserData, storage_device_name: str, find_data_path: bool=True) -> Iterator[tuple[str, GetCollectionPathsResult]]:
    collection_dict: CollectionDict = user_data[COLLECTION_DICT_KEY]
    storage_path_cache: dict[str, str] = {}

    for collection_alias, collection_data in collection_dict.items():
        if storage_device_name in collection_data[STORAGE_DEVICES_KEY]:
            collection_paths = get_collection_paths(user_data, collection_alias, storage_device_name, storage_path_cache, find_data_path)
            yield (collection_alias, collection_paths)


def save_hashset_data(hashset_data: set[str], file_path: str) -> None:
    with open(file_path, 'w') as output:
        for hash_ in sorted(list(hashset_data)):
            output.write(hash_ + '\n')


def load_hashset_data(file_path: str) -> set[str]:
    hashset_data: set[str] = set()

    if os.path.isfile(file_path):
        with open(file_path) as input:
            for line in input.readlines():
                hashset_data.add(strip_crlf(line))

    return hashset_data


def copy_no_overwrite(src: str, dst: str) -> None:
    if os.path.exists(dst):
        raise Exception('copy_no_overwrite')

    shutil.copy(src, dst)


def read_in_chunks(file_object: BufferedReader, size: Optional[int]=None, chunk_size: int=1024*1024) -> Iterator[bytes]:
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M."""

    processed = 0

    while True:
        read_size = chunk_size

        if size is not None:
            read_size = min(read_size, size - processed)

        if read_size <= 0:
            break

        data = file_object.read(read_size)

        if not data:
            break

        processed += len(data)

        yield data


def copy_in_chunks(in_: BufferedReader, out_: BufferedWriter, size: Optional[int]=None, chunk_size: int=1024*1024) -> int:
    processed = 0

    for in_chunk in read_in_chunks(in_, size, chunk_size):
        out_.write(in_chunk)
        processed += len(in_chunk)

    return processed


def parse_ref_line(line: str) -> tuple[str, str]:
    si = line.find(' ')

    if si == -1:
        raise Exception('parse_ref_line')

    return (line[:si], line[si+1:])


class Packer:
    def __init__(self: Packer, in_data: list[tuple[str, str]], out_ref_path: str, out_bin_path: str) -> None:
        self._in_data = in_data
        self._out_ref_path = out_ref_path
        self._out_bin_path = out_bin_path

    def run(self: Packer) -> None:
        with open(self._out_ref_path, 'w') as out_ref:
            with open(self._out_bin_path, 'wb') as out_bin:
                self._copy(out_ref, out_bin)

    def _copy(self: Packer, out_ref: TextIOWrapper, out_bin: BufferedWriter) -> None:
        for in_data_key, in_data_path in self._in_data:
            with open(in_data_path, 'rb') as in_data_file:
                print('Packing ' + in_data_path)
                copy_size = copy_in_chunks(in_data_file, out_bin)
                out_ref.write(str(copy_size) + ' ' + in_data_key + '\n')


class Unpacker:
    def __init__(self: Unpacker, in_data: list[tuple[str, str]], name_provider: Callable[[str], list[str]], unused_hashes_path: str) -> None:
        self._in_data = in_data
        self._name_provider = name_provider
        self._unused_hashes_path = unused_hashes_path

    def run(self: Unpacker) -> None:
        with open(self._unused_hashes_path, 'w') as unused_hashes:
            self._unused_hashes = unused_hashes
            self._unpack_all()

    def _unpack_all(self: Unpacker) -> None:
        for ref_path, bin_path in self._in_data:
            with open(ref_path) as ref:
                with open(bin_path, 'rb') as bin:
                    self._unpack(ref, bin)

    def _unpack(self: Unpacker, ref: TextIOWrapper, bin: BufferedReader) -> None:
        for ref_line in ref.readlines():
            ref_line = strip_crlf(ref_line)
            ref_line = parse_ref_line(ref_line)

            out_size = int(ref_line[0])
            out_key = ref_line[1]
            out_names = self._name_provider(out_key)

            if len(out_names) == 0:
                self._unused_hashes.write(out_key + '\n')
                bin.seek(out_size, 1)
                continue

            out_name = out_names[0]

            if os.path.exists(out_name):
                raise Exception('os.path.exists(out_name)')

            print('Unpacking ' + out_name)

            os.makedirs(os.path.dirname(out_name), exist_ok=True)

            with open(out_name, 'wb') as out:
                if copy_in_chunks(bin, out, out_size) != out_size:
                    raise Exception('copy_in_chunks(bin, out, out_size) != out_size')

            for out_name in out_names[1:]:
                print('Copying ' + out_name)
                os.makedirs(os.path.dirname(out_name), exist_ok=True)
                copy_no_overwrite(out_names[0], out_name)
