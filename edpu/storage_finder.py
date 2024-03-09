from typing import Optional


def get_drive_letters() -> list[str]:
    try:
        import win32api
        return win32api.GetLogicalDriveStrings().split('\000')[:-1]

    except:
        from edpu_user.storage_finder import get_drive_letters
        return get_drive_letters()


def get_path_marker(dir_path: str) -> Optional[str]:
    from os.path import exists

    file_path = dir_path + '.pathmarker'

    if not exists(file_path):
        return None

    with open(file_path, 'r') as file:
        return file.readline().rstrip('\n')


def find_all_storage() -> dict[str, str]:
    dict_: dict[str, str] = {}

    for drive_letter in get_drive_letters():
        path_marker = get_path_marker(drive_letter)
        if path_marker is not None:
            if path_marker in dict_:
                raise Exception('Duplicate path marker ' + path_marker)
            dict_[path_marker] = drive_letter

    return dict_


def keep_getting_storage_path(name: str) -> str:
    while True:
        from .user_interaction import yes_no_prompt

        path = find_all_storage().get(name)

        if path is not None:
            return path

        if not yes_no_prompt('Try to find ' + name + ' again'):
            raise Exception('keep_getting_storage_path ' + name + ' cancelled')


def pick_storage() -> Optional[str]:
    from .user_interaction import pick_option
    storage = find_all_storage()

    if len(storage) == 0:
        print('No storage available')
        return None

    keys = list(storage.keys())
    return keys[pick_option('Pick storage', keys)]
