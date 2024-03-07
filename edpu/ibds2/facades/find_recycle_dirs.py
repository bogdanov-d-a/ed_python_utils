from ..utils.user_data import UserData


def find_recycle_dirs(user_data: UserData) -> None:
    from ..utils.utils import get_storage_device_list

    for storage_device in get_storage_device_list(user_data.storage_devices):
        from ..utils.utils import get_all_aliases_for_storage_device

        print(storage_device)

        for _, collection_paths in get_all_aliases_for_storage_device(user_data, storage_device):
            from os.path import isdir

            recycle_path = collection_paths.get_data() + 'Recycle'

            if isdir(recycle_path):
                from ..utils.walkers import walk_data
                from edpu.file_tree_walker import TYPE_FILE
                from edpu.user_interaction import yes_no_prompt
                from shutil import rmtree

                print(recycle_path + ' exists')

                for recycle_file in sorted(walk_data(recycle_path)[TYPE_FILE]):
                    print(recycle_file)

                if yes_no_prompt('Delete ' + recycle_path):
                    rmtree(recycle_path)