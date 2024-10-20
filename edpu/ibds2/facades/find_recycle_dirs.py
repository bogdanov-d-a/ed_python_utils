from ..utils.user_data import UserData


def find_recycle_dirs(user_data: UserData) -> None:
    from ..utils.utils import get_storage_device_list

    for storage_device in get_storage_device_list(user_data.storage_devices):
        from ..utils.utils import get_all_aliases_for_storage_device

        print(storage_device)

        for _, collection_paths in get_all_aliases_for_storage_device(user_data, storage_device):
            from ..utils.path import RECYCLE_SUFFIX
            from os.path import isdir

            recycle_path = collection_paths.get_data() + RECYCLE_SUFFIX

            if isdir(recycle_path):
                from ...file_tree_walker import TYPE_FILE
                from ...user_interaction import yes_no_prompt
                from ..utils.walkers import walk_data

                print(recycle_path + ' exists')

                for recycle_file in sorted(walk_data(recycle_path, False)[TYPE_FILE]):
                    print(recycle_file)

                if yes_no_prompt('Delete ' + recycle_path):
                    from shutil import rmtree
                    rmtree(recycle_path)
