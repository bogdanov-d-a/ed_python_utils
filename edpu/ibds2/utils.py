import os
from .constants import *
from edpu import file_hashing
from edpu import user_interaction
from edpu import storage_finder


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
    return file_hashing.sha1_file(path)


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
    for main_content in main_list.get(content_type):
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


def handle_all_aliases_for_storage_device(user_data, storage_device_name, handler, find_data_path=True):
    collection_dict = user_data.get(COLLECTION_DICT_KEY)
    storage_path_cache = {}

    for collection_alias, collection_data in collection_dict.items():
        if storage_device_name in collection_data.get(STORAGE_DEVICES_KEY):
            collection_paths = get_collection_paths(user_data, collection_alias, storage_device_name, storage_path_cache, find_data_path)
            handler(collection_alias, collection_paths)
