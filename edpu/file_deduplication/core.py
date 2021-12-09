from .utils import *
from ed_ibds import file_tree_scanner
from ed_ibds import collection_definition
import os
import shutil


def scan_bundles(bundles_path, split_to_dirs):
    bundles_table = {}

    for bundle_path in file_tree_scanner.scan(bundles_path, []):
        if split_to_dirs:
            if len(bundle_path) != 2:
                fail()
            bundle_hash = bundle_path[0] + os.path.splitext(bundle_path[1])[0]
        else:
            if len(bundle_path) != 1:
                fail()
            bundle_hash = os.path.splitext(bundle_path[0])[0]

        if len(bundle_hash) != 40:
            fail()
        bundles_table[bundle_hash] = bundle_path

    return bundles_table


def gen_bundle_path(bundle_hash, split_to_dirs, ext_opt):
    if split_to_dirs:
        bundle_path = [bundle_hash[:2], bundle_hash[2:]]
    else:
        bundle_path = [bundle_hash]

    if ext_opt is not None:
        bundle_path[-1] += ext_opt

    return bundle_path


def save_data_index(data_index, data_index_path):
    collection_definition.save_common_data(sorted(data_index, key=lambda t: t[0]), data_index_path)


def load_data_index(data_index_path):
    return collection_definition.load_common_data(data_index_path)


def copy_no_overwrite(src, dst):
    if os.path.exists(dst):
        fail()
    shutil.copy(src, dst)
