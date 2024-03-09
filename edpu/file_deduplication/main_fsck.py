from .. import file_hashing
from .. import user_interaction
from .fsck import *


def fsck_reachable(bundles_path, split_to_dirs, file_index_paths):
    bundles_hashes = scan_bundles_hashset(bundles_path, split_to_dirs)
    file_index_hashes = get_file_index_files_hashset(file_index_paths)
    missing_hashes = file_index_hashes - bundles_hashes

    for missing_hash in missing_hashes:
        print(missing_hash)
    print('fsck_reachable missing_hashes count = ' + str(len(missing_hashes)))

    return len(missing_hashes)


def fsck_bundles(bundles_path, split_to_dirs, bundles_filter=None):
    bundles = scan_bundles(bundles_path, split_to_dirs)
    hash_errors = []

    for bundle_hash, bundle_path in bundles.items():
        if bundles_filter is not None and bundle_hash not in bundles_filter:
            continue
        bundle_path_abs = os.path.join(bundles_path, os.path.sep.join(bundle_path))
        #print('Hashing ' + bundle_hash)
        if bundle_hash != file_hashing.sha1_file(bundle_path_abs):
            hash_errors.append(bundle_hash)

    for hash_error in hash_errors:
        print(hash_error)
    print('fsck_bundles hash_errors count = ' + str(len(hash_errors)))

    return len(hash_errors)


def fsck(bundles_path, split_to_dirs, file_index_paths):
    fsck_reachable_result = fsck_reachable(bundles_path, split_to_dirs, file_index_paths)
    if fsck_reachable_result != 0:
        return ('fsck_reachable', fsck_reachable_result)

    fsck_bundles_result = fsck_bundles(bundles_path, split_to_dirs, get_file_index_files_hashset(file_index_paths))
    if fsck_bundles_result != 0:
        return ('fsck_bundles', fsck_bundles_result)

    return ('fsck', 0)


def gc_no_fsck(bundles_path, split_to_dirs, file_index_paths):
    bundles = scan_bundles(bundles_path, split_to_dirs)
    bundles_hashes = get_bundles_hashset(bundles)
    file_index_hashes = get_file_index_files_hashset(file_index_paths)
    unreachable_hashes = bundles_hashes - file_index_hashes

    if user_interaction.yes_no_prompt('Delete ' + str(len(unreachable_hashes)) + ' of ' + str(len(bundles_hashes)) + ' bundles?'):
        for unreachable_hash in unreachable_hashes:
            bundle_path = bundles[unreachable_hash]
            bundle_path_abs = os.path.join(bundles_path, os.path.sep.join(bundle_path))
            delete_file_wrapper(bundle_path_abs)


def gc(bundles_path, split_to_dirs, file_index_paths):
    gc_no_fsck(bundles_path, split_to_dirs, file_index_paths)
    fsck_reachable(bundles_path, split_to_dirs, file_index_paths)
