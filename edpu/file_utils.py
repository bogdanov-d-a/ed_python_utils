from typing import Any, Callable


def create_dir_helper(root_dir: str, prefix: str) -> str:
    from os import mkdir
    from os.path import join

    index = None

    while True:
        dir_name = prefix

        if index is not None:
            dir_name += "-" + str(index)

        dir_path = join(root_dir, dir_name)

        try:
            mkdir(dir_path)
            return dir_path
        except:
            pass

        if index is None:
            index = 0
        else:
            index += 1


def create_and_open_dir_with_datetime(root_dir: str) -> None:
    from .datetime_utils import get_now_datetime_str
    from .explorer_launcher import open_dir_in_explorer

    now_datetime_str = get_now_datetime_str()
    dir_path = create_dir_helper(root_dir, now_datetime_str)
    open_dir_in_explorer(dir_path)


def eval_file(filename: str, eval_fn: Callable[[str], Any]=eval) -> Any:
    from codecs import open

    with open(filename, 'r', 'utf-8') as file:
        return eval_fn(file.read())
