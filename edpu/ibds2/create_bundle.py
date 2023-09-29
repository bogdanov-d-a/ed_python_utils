from .utils import *
from .walkers import *
from edpu import datetime_utils
import re


def create_bundle(user_data, storage_device, bundle_alias, collection_alias, bundle_slice_alias):
    storage_path_cache = {}
    collection_paths = get_collection_paths(user_data, collection_alias, storage_device, storage_path_cache)

    def_walk = walk_def(collection_paths.get(DEF_PATH_KEY))
    bundle_slice = user_data.get(COLLECTION_DICT_KEY).get(collection_alias).get(BUNDLE_SLICES_KEY).get(bundle_slice_alias)

    bundle_snap_path = get_bundle_snap_path(user_data, bundle_alias, collection_alias, bundle_slice_alias)
    bundle_snap = load_hashset_data(bundle_snap_path)

    hash_to_data_map = {}

    for def_file in def_walk.get(TYPE_FILE).items():
        def_file_path = def_file[0]
        def_file_hash = def_file[1].get(HASH_KEY)

        if not re.search(bundle_slice, def_file_path):
            continue

        if def_file_hash in bundle_snap:
            continue

        bundle_snap.add(def_file_hash)

        if def_file_hash not in hash_to_data_map:
            hash_to_data_map[def_file_hash] = os.path.join(collection_paths.get(DATA_PATH_KEY), def_file_path)

    bundle_file_path = get_bundle_file_path(user_data, bundle_alias, collection_alias, bundle_slice_alias) + '-' + datetime_utils.get_now_datetime_str()
    Packer(hash_to_data_map.items(), bundle_file_path + '.txt', bundle_file_path + '.bin').run()

    save_hashset_data(bundle_snap, bundle_snap_path)
