import codecs
import os
from typing import Any, Callable
from . import datetime_utils
from . import explorer_launcher

def create_dir_helper(root_dir: str, prefix: str) -> str:
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

def create_and_open_dir_with_datetime(root_dir: str) -> None:
    dt = datetime_utils.get_now_datetime_str()
    dir_path = create_dir_helper(root_dir, dt)
    explorer_launcher.open_dir_in_explorer(dir_path)


def eval_file(filename: str, eval_fn: Callable[[str], Any]=eval) -> Any:
    with codecs.open(filename, 'r', 'utf-8') as file:
        return eval_fn(file.read())
