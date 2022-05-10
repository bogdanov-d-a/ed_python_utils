from .utils import *
from ed_ibds import file_tree_scanner
import codecs
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
    with codecs.open(data_index_path, 'w', 'utf-8-sig') as output:
        for data_index_elem in sorted(data_index, key=lambda t: t[0]):
            if len(data_index_elem) == 2:
                path, hash_ = data_index_elem
            elif len(data_index_elem) == 3:
                path, hash_, mtime = data_index_elem
            else:
                fail()

            if 'mtime' in locals():
                output.write(str(mtime))
                output.write(' ')

            output.write(hash_)
            output.write(' ')
            output.write(path)
            output.write('\n')


def load_data_index(data_index_path, has_mtime):
    with codecs.open(data_index_path, 'r', 'utf-8-sig') as input_:
        data_ = []

        for line in input_.readlines():
            if line[-1] == '\n':
                line = line[:-1]

            parts = line.split(' ', 2 if has_mtime else 1)

            if len(parts) == 2:
                data_.append((parts[1], parts[0]))
            elif len(parts) == 3:
                data_.append((parts[2], parts[1], float(parts[0])))
            else:
                fail()

        return data_


def copy_no_overwrite(src, dst):
    if os.path.exists(dst):
        fail()
    shutil.copy(src, dst)
