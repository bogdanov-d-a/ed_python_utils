from .constants import *
from . import utils
from .walkers import walk_def
from edpu import datetime_utils
import os.path
import re


def create_bundle(user_data: UserData, storage_device: str, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> None:
    storage_path_cache: dict[str, str] = {}
    collection_paths: dict[str, str] = utils.get_collection_paths(user_data, collection_alias, storage_device, storage_path_cache)

    def_walk = walk_def(collection_paths[DEF_PATH_KEY])
    bundle_slice = user_data[COLLECTION_DICT_KEY][collection_alias][BUNDLE_SLICES_KEY][bundle_slice_alias]

    bundle_snap_path = utils.get_bundle_snap_path(user_data, bundle_alias, collection_alias, bundle_slice_alias)
    bundle_snap = utils.load_hashset_data(bundle_snap_path)

    hash_to_data_map: dict[str, str] = {}

    for def_file in def_walk[TYPE_FILE].items():
        def_file_path: str = def_file[0]
        def_file_hash: str = def_file[1][HASH_KEY]

        if not re.search(bundle_slice, def_file_path):
            continue

        if def_file_hash in bundle_snap:
            continue

        bundle_snap.add(def_file_hash)

        if def_file_hash not in hash_to_data_map:
            hash_to_data_map[def_file_hash] = os.path.join(collection_paths[DATA_PATH_KEY], def_file_path)

    bundle_file_path = utils.get_bundle_file_path(user_data, bundle_alias, collection_alias, bundle_slice_alias) + '-' + datetime_utils.get_now_datetime_str()
    utils.Packer(list(hash_to_data_map.items()), bundle_file_path + '.txt', bundle_file_path + '.bin').run()

    utils.save_hashset_data(bundle_snap, bundle_snap_path)
