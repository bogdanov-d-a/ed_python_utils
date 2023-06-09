import os
from edpu import user_interaction
from edpu import pause_at_end
from .constants import *
from .utils import *
from . import update_definition
from . import update_data


def run(user_data):
    def main():
        ACTIONS = [
            'Update definition',
            'Update data',
            'Find recycle dirs',
            'Compare definitions (diff tool)',
        ]

        action = user_interaction.pick_option('Choose an action', ACTIONS)

        if action == 0:
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))
            handle_all_aliases_for_storage_device(
                user_data,
                storage_device,
                lambda _, collection_paths: update_definition.update_definition(collection_paths.get(DATA_PATH_KEY), collection_paths.get(DEF_PATH_KEY), user_data.get(SKIP_MTIME))
            )

        elif action == 1:
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

        elif action == 2:
            storage_device = pick_storage_device(user_data.get(STORAGE_DEVICES_KEY))

            def handler(_, collection_paths):
                recycle_path = collection_paths.get(DATA_PATH_KEY) + 'Recycle'
                if os.path.isdir(recycle_path):
                    print(recycle_path + ' exists')

            handle_all_aliases_for_storage_device(user_data, storage_device, handler)

        elif action == 3:
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

        else:
            raise Exception('unexpected action')

    pause_at_end.run(main, 'Program finished successfully')
