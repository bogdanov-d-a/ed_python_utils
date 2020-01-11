import codecs
import os
import edpu.datetime_utils
import edpu.explorer_launcher

def create_dir_helper(root_dir, prefix):
    index = None

    while True:
        dir_name = prefix
        if index is not None:
            dir_name += "-" + str(index)
        dir_path = os.path.join(root_dir, dir_name)

        try:
            os.mkdir(dir_path)
            return dir_path
        except:
            pass

        if index is None:
            index = 0
        else:
            index += 1

def create_and_open_dir_with_datetime(root_dir):
    dt = edpu.datetime_utils.get_now_datetime_str()
    dir_path = create_dir_helper(root_dir, dt)
    edpu.explorer_launcher.open_dir_in_explorer(dir_path)


def eval_file(filename):
    with codecs.open(filename, 'r', 'utf-8') as file:
        return eval(file.read())
