from ...utils.user_data import UserData


def apply_bundle(user_data: UserData, storage_device: str, collection_alias: str, bundle_slice_alias: str, in_data_items: list[str]) -> None:
    from ...utils.copying_archiver import Unpacker
    from ...utils.path import get_collection_paths
    from ...utils.walkers import walk_def
    from os.path import join

    storage_path_cache: dict[str, str] = {}
    collection_paths = get_collection_paths(user_data, collection_alias, storage_device, storage_path_cache)

    def_walk = walk_def(collection_paths.def_)
    bundle_slice = user_data.collection_dict[collection_alias].bundle_slices[bundle_slice_alias]

    hash_to_data_map: dict[str, list[str]] = {}

    for def_file_path, def_file_data in def_walk.files.items():
        from re import search

        def_file_hash = def_file_data.hash_

        if not search(bundle_slice, def_file_path):
            continue

        if def_file_hash not in hash_to_data_map:
            hash_to_data_map[def_file_hash] = []

        hash_to_data_map[def_file_hash].append(join(collection_paths.get_data(), def_file_path))

    bundles_path = user_data.bundles_path
    in_data = list(map(lambda item: (join(bundles_path, item + '.txt'), join(bundles_path, item + '.bin')), in_data_items))
    unused_hashes_path = join(bundles_path, 'unused_hashes.txt')

    Unpacker(in_data, lambda key: hash_to_data_map.get(key, []), unused_hashes_path).run()
