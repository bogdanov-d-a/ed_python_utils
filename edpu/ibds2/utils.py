import os
import shutil
from .constants import *
from edpu import file_hashing
from edpu import user_interaction
from edpu import storage_finder


def strip_crlf(str_):
    return str_.rstrip('\n').rstrip('\r')


def type_to_prefix(type_):
    if type_ == TYPE_DIR:
        return 'd'
    elif type_ == TYPE_FILE:
        return 'f'
    else:
        raise Exception()


def prefix_to_type(prefix):
    if prefix == 'd':
        return TYPE_DIR
    elif prefix == 'f':
        return TYPE_FILE
    else:
        raise Exception()


def def_path_to_data_path(def_path):
    type_ = prefix_to_type(def_path[-1][0])
    data_path = list(map(lambda a: a[1:], def_path[:-1])) + [def_path[-1][1:]]
    return type_, data_path


def data_path_to_def_path(path_, type_):
    return list(map(lambda a: '_' + a, path_[:-1])) + [type_to_prefix(type_) + path_[-1]]


def hash_file(path):
    print('Calculating hash for ' + path)
    return file_hashing.sha512_file(path)


def getmtime(path):
    return os.path.getmtime(path)


def setmtime(path, time):
    os.utime(path, (time, time))


def path_to_root(path, root):
    return os.path.join(root, os.sep.join(path))


def makedirs_helper(path, root, is_file):
    if is_file:
        if len(path) <= 1:
            return
        path = path[:-1]

    os.makedirs(path_to_root(path, root), exist_ok=True)


def path_to_key(path):
    return INDEX_PATH_SEPARATOR.join(path)


def key_to_path(key):
    return key.split(INDEX_PATH_SEPARATOR)


def intersection_handler(content_type, main_list, aux_list, use_intersection, action):
    for main_content in sorted(main_list.get(content_type)):
        if (main_content in aux_list.get(content_type)) == use_intersection:
            action(key_to_path(main_content))


def get_storage_device_list(storage_devices):
    storage_device_list = []
    for device_name, device_data in storage_devices.items():
        if device_data.get(IS_REMOVABLE_KEY) or device_data.get(IS_SCAN_AVAILABLE_KEY):
            storage_device_list.append(device_name)
    return storage_device_list


def pick_storage_device(storage_devices):
    storage_device_list = get_storage_device_list(storage_devices)
    return storage_device_list[user_interaction.pick_option('Choose storage device', storage_device_list)]


def pick_storage_device_multi(storage_devices):
    storage_device_list = get_storage_device_list(storage_devices)

    result = []
    for picked_index in user_interaction.pick_option_multi('Choose storage devices', storage_device_list):
        result.append(storage_device_list[picked_index])

    return result


def pick_bundle_alias(bundle_aliases):
    bundle_aliases_list = list(sorted(bundle_aliases))
    return bundle_aliases_list[user_interaction.pick_option('Choose bundle alias', bundle_aliases_list)]


def pick_bundle_slice_alias(bundle_slices):
    bundle_slices_list = list(sorted(bundle_slices.keys()))
    return bundle_slices_list[user_interaction.pick_option('Choose bundle slice alias', bundle_slices_list)]


def pick_collection_alias(collection_dict):
    collection_aliases = list(sorted(collection_dict.keys()))
    return collection_aliases[user_interaction.pick_option('Choose collection alias', collection_aliases)]


def get_storage_path(storage_device_name, storage_path_cache):
    storage_path = storage_path_cache.get(storage_device_name)
    if storage_path is not None:
        return storage_path

    storage_path = storage_finder.keep_getting_storage_path(storage_device_name)
    storage_path_cache[storage_device_name] = storage_path
    return storage_path


def get_collection_paths(user_data, collection_alias, storage_device_name, storage_path_cache, find_data_path=True):
    collection_dict = user_data.get(COLLECTION_DICT_KEY)
    storage_devices = user_data.get(STORAGE_DEVICES_KEY)
    data_path = user_data.get(DATA_PATH_KEY)

    collection_data = collection_dict.get(collection_alias)
    collection_storage_devices = collection_data.get(STORAGE_DEVICES_KEY)
    collection_storage_device_data = collection_storage_devices.get(storage_device_name)
    storage_device = storage_devices.get(storage_device_name)

    if find_data_path:
        abs_data_path = collection_storage_device_data
        if storage_device.get(IS_REMOVABLE_KEY):
            abs_data_path = get_storage_path(storage_device_name, storage_path_cache) + abs_data_path
    else:
        abs_data_path = None

    abs_def_path = os.path.join(data_path, collection_alias, storage_device_name)

    return { DEF_PATH_KEY: abs_def_path, DATA_PATH_KEY: abs_data_path }


def get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias):
    return bundle_alias + '-' + collection_alias + '-' + bundle_slice_alias


def get_bundle_file_path(user_data, bundle_alias, collection_alias, bundle_slice_alias):
    return os.path.join(user_data.get(BUNDLES_PATH_KEY), get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias))


def get_bundle_snap_path(user_data, bundle_alias, collection_alias, bundle_slice_alias):
    return os.path.join(user_data.get(BUNDLE_SNAPS_PATH_KEY), get_bundle_file_name(bundle_alias, collection_alias, bundle_slice_alias) + '.txt')


def handle_all_aliases_for_storage_device(user_data, storage_device_name, handler, find_data_path=True):
    collection_dict = user_data.get(COLLECTION_DICT_KEY)
    storage_path_cache = {}

    for collection_alias, collection_data in collection_dict.items():
        if storage_device_name in collection_data.get(STORAGE_DEVICES_KEY):
            collection_paths = get_collection_paths(user_data, collection_alias, storage_device_name, storage_path_cache, find_data_path)
            handler(collection_alias, collection_paths)


def save_hashset_data(hashset_data, file_path):
    with open(file_path, 'w') as output:
        for hash_ in sorted(list(hashset_data)):
            output.write(hash_ + '\n')


def load_hashset_data(file_path):
    hashset_data = set()

    if os.path.isfile(file_path):
        with open(file_path) as input:
            for line in input.readlines():
                hashset_data.add(strip_crlf(line))

    return hashset_data


def copy_no_overwrite(src, dst):
    if os.path.exists(dst):
        raise Exception('copy_no_overwrite')

    shutil.copy(src, dst)


def read_in_chunks(file_object, size=None, chunk_size=1024*1024):
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


def copy_in_chunks(in_, out_, size=None, chunk_size=1024):
    processed = 0

    for in_chunk in read_in_chunks(in_, size, chunk_size):
        out_.write(in_chunk)
        processed += len(in_chunk)

    return processed


def parse_ref_line(line):
    si = line.find(' ')

    if si == -1:
        raise Exception('parse_ref_line')

    return (line[:si], line[si+1:])


class Packer:
    def __init__(self, in_data, out_ref_path, out_bin_path):
        self._in_data = in_data
        self._out_ref_path = out_ref_path
        self._out_bin_path = out_bin_path

    def run(self):
        with open(self._out_ref_path, 'w') as out_ref:
            with open(self._out_bin_path, 'wb') as out_bin:
                self._copy(out_ref, out_bin)

    def _copy(self, out_ref, out_bin):
        for in_data_key, in_data_path in self._in_data:
            with open(in_data_path, 'rb') as in_data_file:
                print('Packing ' + in_data_path)
                copy_size = copy_in_chunks(in_data_file, out_bin)
                out_ref.write(str(copy_size) + ' ' + in_data_key + '\n')


class Unpacker:
    def __init__(self, in_data, name_provider, unused_hashes_path):
        self._in_data = in_data
        self._name_provider = name_provider
        self._unused_hashes_path = unused_hashes_path

    def run(self):
        with open(self._unused_hashes_path, 'w') as unused_hashes:
            self._unused_hashes = unused_hashes
            self._unpack_all()

    def _unpack_all(self):
        for ref_path, bin_path in self._in_data:
            with open(ref_path) as ref:
                with open(bin_path, 'rb') as bin:
                    self._unpack(ref, bin)

    def _unpack(self, ref, bin):
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
