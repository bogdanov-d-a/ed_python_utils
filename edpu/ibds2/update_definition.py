from .walkers import *
from .def_file import save_def_file
from concurrent.futures import ProcessPoolExecutor


def walk_data_with_mutex(path, mutex):
    with mutex:
        return walk_data(path)


def update_definition(root_data_path, root_def_path, skip_mtime, data_mutex):
    with ProcessPoolExecutor(2) as executor:
        data_walk_future = executor.submit(walk_data_with_mutex, root_data_path, data_mutex)
        def_walk_future = executor.submit(walk_def, root_def_path)

        data_walk = data_walk_future.result()
        def_walk = def_walk_future.result()

    getmtime_progress_printer = make_getmtime_progress_printer(root_data_path)

    def path_to_def_root(path):
        return path_to_root(path, root_def_path)

    def path_to_data_root(path):
        return path_to_root(path, root_data_path)

    def def_makedirs_helper(def_path):
        makedirs_helper(def_path, root_def_path, True)

    def debug_remove(path):
        if debug:
            print('debug_remove ' + path)
        else:
            os.remove(path)

    def action_remove(_, def_path):
        debug_remove(path_to_def_root(def_path))

    def action_create_dir(_, def_path):
        def_makedirs_helper(def_path)
        open(path_to_def_root(def_path), 'w')

    def action_create_file(data_path, def_path):
        data_path_abs = path_to_data_root(data_path)
        def_makedirs_helper(def_path)

        with data_mutex:
            save_def_file(path_to_def_root(def_path), hash_file(data_path_abs), getmtime(data_path_abs, getmtime_progress_printer))

    def action_update_file(data_path, def_path):
        if skip_mtime:
            return

        def_data = def_walk.get(TYPE_FILE).get(path_to_key(data_path))
        data_path_abs = path_to_data_root(data_path)

        with data_mutex:
            actual_mtime = getmtime(data_path_abs, getmtime_progress_printer)

            if def_data.get(MTIME_KEY) != actual_mtime:
                save_def_file(path_to_def_root(def_path), hash_file(data_path_abs), actual_mtime)

    def intersection_handler_with_def_path(content_type, main_list, aux_list, use_intersection, action):
        intersection_handler(content_type, main_list, aux_list, use_intersection, lambda data_path: action(data_path, data_path_to_def_path(data_path, content_type)))

    intersection_handler_with_def_path(TYPE_DIR, def_walk, data_walk, False, action_remove)
    intersection_handler_with_def_path(TYPE_DIR, data_walk, def_walk, False, action_create_dir)

    intersection_handler_with_def_path(TYPE_FILE, def_walk, data_walk, False, action_remove)
    intersection_handler_with_def_path(TYPE_FILE, data_walk, def_walk, False, action_create_file)
    intersection_handler_with_def_path(TYPE_FILE, data_walk, def_walk, True, action_update_file)
