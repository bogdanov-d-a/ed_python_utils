from .core import *


def scan_bundles_hashset(bundles_path, split_to_dirs):
    return set(scan_bundles(bundles_path, split_to_dirs).keys())


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
