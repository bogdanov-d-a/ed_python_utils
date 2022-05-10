import os
import shutil
from .walkers import *


def update_data(root_def_path, root_data_path, root_data_path_recycle, data_sources):
    def_walk = walk_def(root_def_path)
    data_walk = walk_data(root_data_path)

    data_source_hash_to_location = {}
    for data_source_def_path, data_source_data_path in data_sources:
        data_source_def = walk_def(data_source_def_path).get(TYPE_FILE)
        for path_, data in data_source_def.items():
            hash_ = data.get(HASH_KEY)
            if hash_ not in data_source_hash_to_location:
                data_source_hash_to_location[hash_] = (key_to_path(path_), data_source_data_path)

    recycle_file_lists = {}

    def path_to_data_root(path):
        return path_to_root(path, root_data_path)

    def path_to_data_recycle_root(path):
        return path_to_root(path, root_data_path_recycle)

    def data_recycle_makedirs_helper(data_path):
        makedirs_helper(data_path, root_data_path_recycle, True)

    def find_file_by_hash(hash_):
        recycle_files = recycle_file_lists.get(hash_)
        if recycle_files is not None:
            recycle_file = recycle_files[0]
            recycle_file_lists[hash_] = recycle_files[1:]
            return (path_to_data_root(recycle_file), True)

        data_source_location = data_source_hash_to_location.get(hash_)
        if data_source_location is not None:
            return (path_to_root(data_source_location[0], data_source_location[1]), False)

        return (None, None)

    def copy_no_overwrite(src, dst):
        if os.path.exists(dst):
            raise Exception()

        print('Copying ' + src + ' to ' + dst)
        shutil.copy(src, dst)

    def copy_or_move_file(src, dst, move):
        if not move:
            copy_no_overwrite(src, dst)
        else:
            os.rename(src, dst)

    def move_for_recycling(path_):
        os.makedirs(root_data_path_recycle, exist_ok=True)
        data_recycle_makedirs_helper(path_)
        os.rename(path_to_data_root(path_), path_to_data_recycle_root(path_))

    def action_create_dir(data_path):
        makedirs_helper(data_path, root_data_path, False)

    def action_recycle_file(data_path):
        data_path_abs = path_to_data_root(data_path)
        hash_ = hash_file(data_path_abs)
        if hash_ not in recycle_file_lists:
            recycle_file_lists[hash_] = []
        recycle_file_lists.get(hash_).append(data_path)

    def action_create_file(data_path):
        def_walk_data = def_walk.get(TYPE_FILE).get(path_to_key(data_path))

        file_by_hash, can_move = find_file_by_hash(def_walk_data.get(HASH_KEY))
        if file_by_hash is None:
            print('File not found, hash ' + def_walk_data.get(HASH_KEY))
            return

        data_path_abs = path_to_data_root(data_path)
        copy_or_move_file(file_by_hash, data_path_abs, can_move)
        setmtime(data_path_abs, def_walk_data.get(MTIME_KEY))

    def action_update_file(data_path):
        data_path_abs = path_to_data_root(data_path)
        def_walk_data = def_walk.get(TYPE_FILE).get(path_to_key(data_path))

        if def_walk_data.get(MTIME_KEY) != getmtime(data_path_abs):
            if hash_file(data_path_abs) != def_walk_data.get(HASH_KEY):
                file_by_hash, can_move = find_file_by_hash(def_walk_data.get(HASH_KEY))
                if file_by_hash is None:
                    print('File not found, hash ' + def_walk_data.get(HASH_KEY))
                    return

                move_for_recycling(data_path)
                copy_or_move_file(file_by_hash, data_path_abs, can_move)

            setmtime(data_path_abs, def_walk_data.get(MTIME_KEY))

    def action_remove_empty_dir(data_path):
        data_path_abs = path_to_data_root(data_path)
        try:
            os.rmdir(data_path_abs)
        except:
            pass

    intersection_handler(TYPE_DIR, def_walk, data_walk, False, action_create_dir)

    intersection_handler(TYPE_FILE, data_walk, def_walk, False, action_recycle_file)
    intersection_handler(TYPE_FILE, def_walk, data_walk, False, action_create_file)
    intersection_handler(TYPE_FILE, def_walk, data_walk, True, action_update_file)

    for recycle_files in recycle_file_lists.values():
        for recycle_file in recycle_files:
            move_for_recycling(recycle_file)

    intersection_handler(TYPE_DIR, data_walk, def_walk, False, action_remove_empty_dir)
