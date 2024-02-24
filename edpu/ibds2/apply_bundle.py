from .constants import *
from .walkers import walk_def
from . import utils
import os.path
import re


def apply_bundle(user_data: UserData, storage_device: str, collection_alias: str, bundle_slice_alias: str, in_data_items: list[str]) -> None:
    storage_path_cache: dict[str, str] = {}
    collection_paths: dict[str, str] = utils.get_collection_paths(user_data, collection_alias, storage_device, storage_path_cache)

    def_walk = walk_def(collection_paths[DEF_PATH_KEY])
    bundle_slice = user_data[COLLECTION_DICT_KEY][collection_alias][BUNDLE_SLICES_KEY][bundle_slice_alias]

    hash_to_data_map: dict[str, list[str]] = {}

    for def_file_path, def_file_data in def_walk.files.items():
        def_file_hash = def_file_data.hash_

        if not re.search(bundle_slice, def_file_path):
            continue

        if def_file_hash not in hash_to_data_map:
            hash_to_data_map[def_file_hash] = []

        hash_to_data_map[def_file_hash].append(os.path.join(collection_paths[DATA_PATH_KEY], def_file_path))

    bundles_path = user_data[BUNDLES_PATH_KEY]
    in_data = list(map(lambda item: (os.path.join(bundles_path, item + '.txt'), os.path.join(bundles_path, item + '.bin')), in_data_items))
    unused_hashes_path = os.path.join(bundles_path, 'unused_hashes.txt')

    def name_provider(key: str) -> list[str]:
        d = hash_to_data_map.get(key)
        return [] if d is None else d

    utils.Unpacker(in_data, name_provider, unused_hashes_path).run()
