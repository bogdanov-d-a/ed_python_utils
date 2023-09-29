from .utils import *
from .walkers import *
import re


def apply_bundle(user_data, storage_device, collection_alias, bundle_slice_alias, in_data_items):
    storage_path_cache = {}
    collection_paths = get_collection_paths(user_data, collection_alias, storage_device, storage_path_cache)

    def_walk = walk_def(collection_paths.get(DEF_PATH_KEY))
    bundle_slice = user_data.get(COLLECTION_DICT_KEY).get(collection_alias).get(BUNDLE_SLICES_KEY).get(bundle_slice_alias)

    hash_to_data_map = {}

    for def_file in def_walk.get(TYPE_FILE).items():
        def_file_path = def_file[0]
        def_file_hash = def_file[1].get(HASH_KEY)

        if not re.search(bundle_slice, def_file_path):
            continue

        if def_file_hash not in hash_to_data_map:
            hash_to_data_map[def_file_hash] = []

        hash_to_data_map[def_file_hash].append(os.path.join(collection_paths.get(DATA_PATH_KEY), def_file_path))

    bundles_path = user_data.get(BUNDLES_PATH_KEY)
    in_data = list(map(lambda item: (os.path.join(bundles_path, item + '.txt'), os.path.join(bundles_path, item + '.bin')), in_data_items))
    unused_hashes_path = os.path.join(bundles_path, 'unused_hashes.txt')

    def name_provider(key):
        d = hash_to_data_map.get(key)
        return [] if d is None else d

    Unpacker(in_data, name_provider, unused_hashes_path).run()
