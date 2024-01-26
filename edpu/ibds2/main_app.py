import operator
import os
from edpu import user_interaction
from edpu import pause_at_end
from .constants import *
from .utils import *
from . import update_definition
from . import update_data
from . import create_bundle
from . import apply_bundle


def run(user_data):
    def main():
        def action_update_definition():
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))

            handle_all_aliases_for_storage_device(
                user_data,
                storage_device,
                lambda _, collection_paths: update_definition.update_definition(collection_paths.get(DATA_PATH_KEY), collection_paths.get(DEF_PATH_KEY), user_data.get(SKIP_MTIME))
            )

        def action_update_data():
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            source_storage_devices = pick_storage_device_multi(user_data.get(STORAGE_DEVICES_KEY))

            collection_dict = user_data.get(COLLECTION_DICT_KEY)
            storage_path_cache = {}

            def data_sources_provider(collection_alias):
                collection_data = collection_dict.get(collection_alias)
                data_sources = []

                for source_storage_device in source_storage_devices:
                    if source_storage_device in collection_data.get(STORAGE_DEVICES_KEY):
                        collection_paths = get_collection_paths(user_data, collection_alias, source_storage_device, storage_path_cache)
                        data_sources.append((collection_paths.get(DEF_PATH_KEY), collection_paths.get(DATA_PATH_KEY)))

                return data_sources

            handle_all_aliases_for_storage_device(
                user_data,
                storage_device,
                lambda collection_alias, collection_paths: update_data.update_data(collection_paths.get(DEF_PATH_KEY), collection_paths.get(DATA_PATH_KEY), collection_paths.get(DATA_PATH_KEY) + 'Recycle', data_sources_provider(collection_alias))
            )

        def action_find_recycle_dirs():
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))

            def handler(_, collection_paths):
                recycle_path = collection_paths.get(DATA_PATH_KEY) + 'Recycle'
                if os.path.isdir(recycle_path):
                    print(recycle_path + ' exists')

            handle_all_aliases_for_storage_device(user_data, storage_device, handler)

        def action_compare_definitions():
            storage_device_a = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            storage_device_b = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))

            diff_tool_handler = user_data.get(DIFF_TOOL_HANDLER)

            def get_def_paths(storage_device):
                result = {}

                def handler(collection_alias, collection_paths):
                    result[collection_alias] = collection_paths.get(DEF_PATH_KEY)

                handle_all_aliases_for_storage_device(user_data, storage_device, handler, find_data_path=False)

                return result

            def_paths_a = get_def_paths(storage_device_a)
            def_paths_b = get_def_paths(storage_device_b)

            for collection_alias in sorted(set(def_paths_a.keys()).intersection(set(def_paths_b.keys()))):
                diff_tool_handler(def_paths_a.get(collection_alias), def_paths_b.get(collection_alias))

        def action_create_bundle():
            collection_dict = user_data.get(COLLECTION_DICT_KEY)

            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            bundle_alias = pick_bundle_alias(user_data.get(BUNDLE_ALIASES_KEY))
            collection_alias = pick_collection_alias(collection_dict)
            bundle_slice_alias = pick_bundle_slice_alias(collection_dict.get(collection_alias).get(BUNDLE_SLICES_KEY))

            create_bundle.create_bundle(user_data, storage_device, bundle_alias, collection_alias, bundle_slice_alias)

        def action_apply_bundle():
            collection_dict = user_data.get(COLLECTION_DICT_KEY)

            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            collection_alias = pick_collection_alias(collection_dict)
            bundle_slice_alias = pick_bundle_slice_alias(collection_dict.get(collection_alias).get(BUNDLE_SLICES_KEY))

            apply_bundle.apply_bundle(user_data, storage_device, collection_alias, bundle_slice_alias, user_data.get(APPLY_BUNDLES_KEY))

        ACTIONS = [
            ('Update definition', action_update_definition),
            ('Update data', action_update_data),
            ('Find recycle dirs', action_find_recycle_dirs),
            ('Compare definitions (diff tool)', action_compare_definitions),
            ('Create bundle', action_create_bundle),
            ('Apply bundle', action_apply_bundle),
        ]

        action = user_interaction.pick_option('Choose an action', list(map(operator.itemgetter(0), ACTIONS)))

        if action < len(ACTIONS):
            ACTIONS[action][1]()
        else:
            raise Exception('unexpected action')

    pause_at_end.run(main, 'Program completed successfully')
