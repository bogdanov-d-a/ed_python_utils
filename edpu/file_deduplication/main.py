from .core import *
from edpu import file_hashing
from edpu import file_tree_walker
import os


DATA_INDEX_SEPARATOR = '\\'


def copy_data_to_bundles(data_path, bundles_path, file_index_path, dir_index_path, save_mtime, split_to_dirs, keep_ext):
    if os.path.exists(file_index_path):
        fail()

    if dir_index_path is not None and (os.path.exists(dir_index_path) or file_index_path == dir_index_path):
        fail()

    walk_result = file_tree_walker.walk(
        data_path,
        lambda type, _: type == file_tree_walker.TYPE_DIR and dir_index_path is None
    )

    if dir_index_path is not None:
        dir_index = []

        for data_path_item in walk_result.get(file_tree_walker.TYPE_DIR):
            dir_index.append(DATA_INDEX_SEPARATOR.join(data_path_item))

        save_dir_index(dir_index, dir_index_path)

    bundles = scan_bundles(bundles_path, split_to_dirs)
    file_index = []

    for data_path_item in walk_result.get(file_tree_walker.TYPE_FILE):
        data_path_item_abs = os.path.join(data_path, os.path.sep.join(data_path_item))
        print('Hashing ' + DATA_INDEX_SEPARATOR.join(data_path_item))
        bundle_hash = file_hashing.sha1_file(data_path_item_abs)

        if save_mtime:
            file_index.append((DATA_INDEX_SEPARATOR.join(data_path_item), bundle_hash, os.path.getmtime(data_path_item_abs)))
        else:
            file_index.append((DATA_INDEX_SEPARATOR.join(data_path_item), bundle_hash))

        if bundle_hash not in bundles:
            bundles[bundle_hash] = gen_bundle_path(bundle_hash, split_to_dirs, os.path.splitext(data_path_item[-1])[1] if keep_ext else None)
            bundle_path_abs = os.path.join(bundles_path, os.path.sep.join(bundles[bundle_hash]))
            if split_to_dirs:
                os.makedirs(os.path.dirname(bundle_path_abs), exist_ok=True)
            print('Copying ' + bundle_hash)
            copy_no_overwrite(data_path_item_abs, bundle_path_abs)

    save_file_index(file_index, file_index_path)


def recreate_data_from_bundles(bundles_path, split_to_dirs, file_index_path, dir_index_path, recreate_data_path, restore_mtime):
    bundles = scan_bundles(bundles_path, split_to_dirs)
    file_index = load_file_index(file_index_path, restore_mtime)
    if dir_index_path is not None:
        dir_index = load_dir_index(dir_index_path)
    os.makedirs(recreate_data_path)

    if dir_index_path is not None:
        for dir_index_elem in dir_index:
            dir_index_elem_abs = os.path.join(recreate_data_path, os.path.sep.join(dir_index_elem.split(DATA_INDEX_SEPARATOR)))
            os.makedirs(dir_index_elem_abs, exist_ok=True)

    for file_index_elem in file_index:
        if restore_mtime:
            file_index_item_path, file_index_item_hash, file_index_item_mtime = file_index_elem
        else:
            file_index_item_path, file_index_item_hash = file_index_elem

        file_index_item_path_abs = os.path.join(recreate_data_path, os.path.sep.join(file_index_item_path.split(DATA_INDEX_SEPARATOR)))
        os.makedirs(os.path.dirname(file_index_item_path_abs), exist_ok=True)
        print('Copying ' + file_index_item_path)
        copy_no_overwrite(os.path.join(bundles_path, os.path.sep.join(bundles[file_index_item_hash])), file_index_item_path_abs)
        if restore_mtime:
            os.utime(file_index_item_path_abs, (file_index_item_mtime, file_index_item_mtime))


def backup_and_recover(backup_path, restore_path, bundles_path, file_index_path, dir_index_path, save_mtime, split_to_dirs, keep_ext):
    print('copy_data_to_bundles')
    copy_data_to_bundles(backup_path, bundles_path, file_index_path, dir_index_path, save_mtime, split_to_dirs, keep_ext)

    print('recreate_data_from_bundles')
    recreate_data_from_bundles(bundles_path, split_to_dirs, file_index_path, dir_index_path, restore_path, save_mtime)
