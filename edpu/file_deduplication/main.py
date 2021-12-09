from .core import *
from ed_ibds import hash_facade


def copy_data_to_bundles(data_path, bundles_path, data_index_path, split_to_dirs, keep_ext):
    if os.path.exists(data_index_path):
        fail()

    bundles = scan_bundles(bundles_path, split_to_dirs)
    data_index = []

    for data_path_item in file_tree_scanner.scan(data_path, []):
        data_path_item_abs = os.path.join(data_path, '\\'.join(data_path_item))
        bundle_hash = hash_facade.sha1(data_path_item_abs)
        data_index.append(('\\'.join(data_path_item), bundle_hash))

        if bundle_hash not in bundles:
            bundles[bundle_hash] = gen_bundle_path(bundle_hash, split_to_dirs, os.path.splitext(data_path_item[-1])[1] if keep_ext else None)
            bundle_path_abs = os.path.join(bundles_path, '\\'.join(bundles[bundle_hash]))
            if split_to_dirs:
                os.makedirs(os.path.dirname(bundle_path_abs), exist_ok=True)
            print('Copying ' + '\\'.join(data_path_item))
            copy_no_overwrite(data_path_item_abs, bundle_path_abs)

    save_data_index(data_index, data_index_path)


def recreate_data_from_bundles(bundles_path, split_to_dirs, data_index_path, recreate_data_path):
    bundles = scan_bundles(bundles_path, split_to_dirs)
    data_index = load_data_index(data_index_path)
    os.makedirs(recreate_data_path)
    for data_index_item_path, data_index_item_hash in data_index:
        data_index_item_path_abs = os.path.join(recreate_data_path, data_index_item_path)
        os.makedirs(os.path.dirname(data_index_item_path_abs), exist_ok=True)
        print('Copying ' + data_index_item_path)
        copy_no_overwrite(os.path.join(bundles_path, '\\'.join(bundles[data_index_item_hash])), data_index_item_path_abs)


def backup_and_recover(backup_path, restore_path, bundles_path, data_index_path, split_to_dirs, keep_ext):
    print('copy_data_to_bundles')
    copy_data_to_bundles(backup_path, bundles_path, data_index_path, split_to_dirs, keep_ext)

    print('recreate_data_from_bundles')
    recreate_data_from_bundles(bundles_path, split_to_dirs, data_index_path, restore_path)
