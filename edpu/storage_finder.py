import os
from . import user_interaction

try:
    import win32api
    win32api_loaded = True
except:
    import edpu_user.storage_finder
    win32api_loaded = False


def get_drive_letters():
    return win32api.GetLogicalDriveStrings().split('\000')[:-1] if win32api_loaded else edpu_user.storage_finder.get_drive_letters()


def get_path_marker(dir_path):
    file_path = dir_path + '.pathmarker'

    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as file:
        return file.readline().rstrip('\n')


def find_all_storage():
    dict_ = {}

    for drive_letter in get_drive_letters():
        path_marker = get_path_marker(drive_letter)
        if path_marker is not None:
            if path_marker in dict_:
                raise Exception('Duplicate path marker ' + path_marker)
            dict_[path_marker] = drive_letter

    return dict_


def keep_getting_storage_path(name):
    while True:
        path = find_all_storage().get(name)

        if path is not None:
            return path

        if not user_interaction.yes_no_prompt('Try to find ' + name + ' again'):
            return None


def pick_storage():
    storage = find_all_storage()
    if len(storage) == 0:
        print('No storage available')
        return None
    keys = list(storage.keys())
    return keys[user_interaction.pick_option('Pick storage', keys)]
