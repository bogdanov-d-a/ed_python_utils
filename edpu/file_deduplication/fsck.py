from .core import *
import os


def get_bundles_hashset(bundles):
    return set(bundles.keys())


def scan_bundles_hashset(bundles_path, split_to_dirs):
    return get_bundles_hashset(scan_bundles(bundles_path, split_to_dirs))


def get_data_index_hashset(data_index):
    hashes = set()
    for _, data_index_item_hash in data_index:
        hashes.add(data_index_item_hash)
    return hashes


def get_data_index_files_hashset(data_index_paths):
    hashes = set()
    for data_index_path in data_index_paths:
        hashes |= get_data_index_hashset(load_data_index(data_index_path))
    return hashes


def delete_file_wrapper(path):
    delete_file_debug = False
    if delete_file_debug:
        print('delete_file_wrapper path = ' + path)
    else:
        os.remove(path)
