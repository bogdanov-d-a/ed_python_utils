from .core import *
import os


def get_bundles_hashset(bundles):
    return set(bundles.keys())


def scan_bundles_hashset(bundles_path, split_to_dirs):
    return get_bundles_hashset(scan_bundles(bundles_path, split_to_dirs))


def get_file_index_hashset(file_index):
    hashes = set()
    for _, file_index_item_hash in file_index:
        hashes.add(file_index_item_hash)
    return hashes


def get_file_index_files_hashset(file_index_paths):
    hashes = set()
    for file_index_path in file_index_paths:
        hashes |= get_file_index_hashset(load_file_index(file_index_path))
    return hashes


def delete_file_wrapper(path):
    delete_file_debug = False
    if delete_file_debug:
        print('delete_file_wrapper path = ' + path)
    else:
        os.remove(path)
