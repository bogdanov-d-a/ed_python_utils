from ...utils.user_data import UserData


def create_bundle(user_data: UserData, storage_device: str, bundle_alias: str, collection_alias: str, bundle_slice_alias: str) -> None:
    from ....datetime_utils import get_now_datetime_str
    from ...utils import hashset, path
    from ...utils.copying_archiver import Packer
    from ...utils.walkers import walk_def

    storage_path_cache: dict[str, str] = {}
    collection_paths = path.get_collection_paths(user_data, collection_alias, storage_device, storage_path_cache)

    def_walk = walk_def(collection_paths.def_)
    bundle_slice = user_data.collection_dict[collection_alias].bundle_slices[bundle_slice_alias]

    bundle_snap_path = path.get_bundle_snap_path(user_data, bundle_alias, collection_alias, bundle_slice_alias)
    bundle_snap = hashset.load(bundle_snap_path)

    hash_to_data_map: dict[str, str] = {}

    for def_file_path, def_file_data in def_walk.files.items():
        from re import search

        def_file_hash = def_file_data.hash_

        if not search(bundle_slice, def_file_path):
            continue

        if def_file_hash in bundle_snap:
            continue

        bundle_snap.add(def_file_hash)

        if def_file_hash not in hash_to_data_map:
            from os.path import join
            hash_to_data_map[def_file_hash] = join(collection_paths.get_data(), def_file_path)

    bundle_file_path = path.get_bundle_file_path(user_data, bundle_alias, collection_alias, bundle_slice_alias) + '-' + get_now_datetime_str()
    Packer(list(hash_to_data_map.items()), bundle_file_path + '.txt', bundle_file_path + '.bin').run()

    hashset.save(bundle_snap, bundle_snap_path)
