import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from typing import Callable
from edpu.file_tree_walker import TYPE_FILE
from edpu import guided_directory_use
from edpu import pause_at_end
from edpu import user_interaction
from .constants import *
from . import utils
from . import apply_bundle
from . import compare_definitions
from . import create_bundle
from . import update_data
from . import update_definition
from . import utils
from . import walkers


def same_defs_helper(args: tuple[str, str]) -> bool:
    path_a, path_b = args
    return compare_definitions.same_defs(path_a, path_b)


def run(user_data: UserData) -> None:
    def main() -> None:
        def action_update_definition() -> None:
            storage_device = utils.pick_storage_device(user_data[STORAGE_DEVICES_KEY])
            aliases = list(utils.get_all_aliases_for_storage_device(user_data, storage_device))

            manager = Manager()
            data_mutex = manager.Lock()

            with ProcessPoolExecutor(min(len(aliases), user_data[COLLECTION_PROCESSING_WORKERS])) as executor:
                futures = list(map(
                    lambda alias: executor.submit(
                        update_definition.update_definition,
                        alias[1].get_data(),
                        alias[1].def_,
                        user_data[SKIP_MTIME],
                        data_mutex
                    ),
                    aliases
                ))

                for future in futures:
                    future.result()

        def action_update_data() -> None:
            storage_device = utils.pick_storage_device(user_data[STORAGE_DEVICES_KEY])
            source_storage_devices = utils.pick_storage_device_multi(user_data[STORAGE_DEVICES_KEY])

            aliases = list(utils.get_all_aliases_for_storage_device(user_data, storage_device))

            storage_path_cache: dict[str, str] = {}

            def data_sources_provider(collection_alias: str) -> list[tuple[str, str]]:
                collection_data = user_data[COLLECTION_DICT_KEY][collection_alias]
                data_sources: list[tuple[str, str]] = []

                for source_storage_device in source_storage_devices:
                    if source_storage_device in collection_data[STORAGE_DEVICES_KEY]:
                        collection_paths = utils.get_collection_paths(user_data, collection_alias, source_storage_device, storage_path_cache)
                        data_sources.append((collection_paths.def_, collection_paths.get_data()))

                return data_sources

            manager = Manager()
            data_mutex = manager.Lock()

            with ProcessPoolExecutor(min(len(aliases), user_data[COLLECTION_PROCESSING_WORKERS])) as executor:
                futures = list(map(
                    lambda alias: executor.submit(
                        update_data.update_data,
                        alias[1].def_,
                        alias[1].get_data(),
                        alias[1].get_data() + 'Recycle',
                        data_sources_provider(alias[0]),
                        data_mutex
                    ),
                    aliases
                ))

                for future in futures:
                    future.result()

        def action_find_recycle_dirs() -> None:
            for storage_device in utils.get_storage_device_list(user_data[STORAGE_DEVICES_KEY]):
                print(storage_device)

                for _, collection_paths in utils.get_all_aliases_for_storage_device(user_data, storage_device):
                    recycle_path = collection_paths.get_data() + 'Recycle'

                    if os.path.isdir(recycle_path):
                        print(recycle_path + ' exists')

                        for recycle_file in sorted(walkers.walk_data(recycle_path)[TYPE_FILE]):
                            print(recycle_file)

                        if user_interaction.yes_no_prompt('Delete ' + recycle_path):
                            shutil.rmtree(recycle_path)

        def action_compare_definitions() -> None:
            storage_device_a = utils.pick_storage_device(user_data[STORAGE_DEVICES_KEY])
            storage_device_b = utils.pick_storage_device(user_data[STORAGE_DEVICES_KEY])

            diff_tool_handler = user_data[DIFF_TOOL_HANDLER]

            def get_def_paths(storage_device: str) -> dict[str, str]:
                return {
                    collection_alias: collection_paths.def_
                    for collection_alias, collection_paths
                    in utils.get_all_aliases_for_storage_device(user_data, storage_device, find_data_path=False)
                }

            def_paths_a = get_def_paths(storage_device_a)
            def_paths_b = get_def_paths(storage_device_b)

            def_paths_list = list(map(
                lambda collection_alias: [def_paths_a[collection_alias], def_paths_b[collection_alias]],
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

        def action_create_bundle() -> None:
            def bundles_path_callback(_) -> None:
                storage_device = utils.pick_storage_device(user_data[STORAGE_DEVICES_KEY])
                bundle_alias = utils.pick_bundle_alias(utils.get_bundle_aliases(user_data))

                for collection_alias, collection_data in user_data[COLLECTION_DICT_KEY].items():
                    if bundle_alias not in collection_data[BUNDLE_ALIASES_KEY]:
                        continue

                    for bundle_slice_alias in collection_data[BUNDLE_ALIASES_KEY][bundle_alias]:
                        create_bundle.create_bundle(user_data, storage_device, bundle_alias, collection_alias, bundle_slice_alias)
                        print(collection_alias + ' - ' + bundle_slice_alias)
                        input()

            guided_directory_use.run_with_path(user_data[BUNDLES_PATH_KEY], bundles_path_callback)

        def action_apply_bundle() -> None:
            collection_dict = user_data[COLLECTION_DICT_KEY]

            storage_device = utils.pick_storage_device(user_data[STORAGE_DEVICES_KEY])
            collection_alias = utils.pick_collection_alias(collection_dict)
            bundle_slice_alias = utils.pick_bundle_slice_alias(collection_dict[collection_alias][BUNDLE_SLICES_KEY])

            apply_bundle.apply_bundle(user_data, storage_device, collection_alias, bundle_slice_alias, user_data[APPLY_BUNDLES_KEY])

        actions: list[tuple[str, str, Callable[[], None]]] = [
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
