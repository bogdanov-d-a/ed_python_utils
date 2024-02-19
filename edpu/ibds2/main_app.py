import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from edpu.file_tree_walker import TYPE_FILE
from edpu import pause_at_end
from edpu import user_interaction
from .constants import *
from .utils import *
from . import apply_bundle
from . import compare_definitions
from . import create_bundle
from . import update_data
from . import update_definition
from . import utils
from . import walkers


def same_defs_helper(args):
    path_a, path_b = args
    return compare_definitions.same_defs(path_a, path_b)


def run(user_data):
    def main():
        def action_update_definition():
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            aliases = list(get_all_aliases_for_storage_device(user_data, storage_device))

            manager = Manager()
            data_mutex = manager.Lock()

            with ProcessPoolExecutor(min(len(aliases), user_data[COLLECTION_PROCESSING_WORKERS])) as executor:
                futures = list(map(
                    lambda alias: executor.submit(
                        update_definition.update_definition,
                        alias[1].get(DATA_PATH_KEY),
                        alias[1].get(DEF_PATH_KEY),
                        user_data.get(SKIP_MTIME),
                        data_mutex
                    ),
                    aliases
                ))

                for future in futures:
                    future.result()

        def action_update_data():
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            source_storage_devices = pick_storage_device_multi(user_data.get(STORAGE_DEVICES_KEY))

            aliases = list(get_all_aliases_for_storage_device(user_data, storage_device))

            storage_path_cache = {}

            def data_sources_provider(collection_alias):
                collection_data = user_data.get(COLLECTION_DICT_KEY).get(collection_alias)
                data_sources = []

                for source_storage_device in source_storage_devices:
                    if source_storage_device in collection_data.get(STORAGE_DEVICES_KEY):
                        collection_paths = get_collection_paths(user_data, collection_alias, source_storage_device, storage_path_cache)
                        data_sources.append((collection_paths.get(DEF_PATH_KEY), collection_paths.get(DATA_PATH_KEY)))

                return data_sources

            manager = Manager()
            data_mutex = manager.Lock()

            with ProcessPoolExecutor(min(len(aliases), user_data[COLLECTION_PROCESSING_WORKERS])) as executor:
                futures = list(map(
                    lambda alias: executor.submit(
                        update_data.update_data,
                        alias[1].get(DEF_PATH_KEY),
                        alias[1].get(DATA_PATH_KEY),
                        alias[1].get(DATA_PATH_KEY) + 'Recycle',
                        data_sources_provider(alias[0]),
                        data_mutex
                    ),
                    aliases
                ))

                for future in futures:
                    future.result()

        def action_find_recycle_dirs():
            for storage_device in utils.get_storage_device_list(user_data.get(STORAGE_DEVICES_KEY)):
                print(storage_device)

                for _, collection_paths in get_all_aliases_for_storage_device(user_data, storage_device):
                    recycle_path = collection_paths.get(DATA_PATH_KEY) + 'Recycle'

                    if os.path.isdir(recycle_path):
                        print(recycle_path + ' exists')

                        for recycle_file in sorted(walkers.walk_data(recycle_path)[TYPE_FILE]):
                            print(recycle_file)

                        if user_interaction.yes_no_prompt('Delete ' + recycle_path):
                            shutil.rmtree(recycle_path)

        def action_compare_definitions():
            storage_device_a = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            storage_device_b = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))

            diff_tool_handler = user_data.get(DIFF_TOOL_HANDLER)

            def get_def_paths(storage_device):
                return {
                    collection_alias: collection_paths.get(DEF_PATH_KEY)
                    for collection_alias, collection_paths
                    in get_all_aliases_for_storage_device(user_data, storage_device, find_data_path=False)
                }

            def_paths_a = get_def_paths(storage_device_a)
            def_paths_b = get_def_paths(storage_device_b)

            def_paths_list = list(map(
                lambda collection_alias: [def_paths_a.get(collection_alias), def_paths_b.get(collection_alias)],
                sorted(set(def_paths_a.keys()).intersection(set(def_paths_b.keys())))
            ))

            with ProcessPoolExecutor(min(len(def_paths_list), user_data[COLLECTION_PROCESSING_WORKERS])) as executor:
                same_defs_list = list(executor.map(
                    same_defs_helper,
                    def_paths_list
                ))

            for def_paths, same_defs in zip(def_paths_list, same_defs_list):
                if not same_defs:
                    diff_tool_handler(def_paths[0], def_paths[1])

        def action_create_bundle():
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            bundle_alias = pick_bundle_alias(get_bundle_aliases(user_data))

            for collection_alias, collection_data in user_data[COLLECTION_DICT_KEY].items():
                if bundle_alias not in collection_data[BUNDLE_ALIASES_KEY]:
                    continue

                for bundle_slice_alias in collection_data[BUNDLE_ALIASES_KEY][bundle_alias]:
                    create_bundle.create_bundle(user_data, storage_device, bundle_alias, collection_alias, bundle_slice_alias)
                    print(collection_alias + ' - ' + bundle_slice_alias)
                    input()

        def action_apply_bundle():
            collection_dict = user_data.get(COLLECTION_DICT_KEY)

            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            collection_alias = pick_collection_alias(collection_dict)
            bundle_slice_alias = pick_bundle_slice_alias(collection_dict.get(collection_alias).get(BUNDLE_SLICES_KEY))

            apply_bundle.apply_bundle(user_data, storage_device, collection_alias, bundle_slice_alias, user_data.get(APPLY_BUNDLES_KEY))

        actions = [
            ('s', 'Update definition', action_update_definition),
            ('u', 'Update data', action_update_data),
            ('r', 'Find recycle dirs', action_find_recycle_dirs),
            ('c', 'Compare definitions (diff tool)', action_compare_definitions),
            ('bc', 'Create bundle', action_create_bundle),
            ('ba', 'Apply bundle', action_apply_bundle),
        ]

        action = user_interaction.pick_str_option_ex('Choose an action', actions)
        action()

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
