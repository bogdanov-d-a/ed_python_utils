import os
import os.path
from typing import Callable


def mkdir(path_: str) -> None:
    if os.path.exists(path_):
        raise Exception(path_ + ' exists')

    os.mkdir(path_)


def remove(path_: str) -> None:
    while True:
        print('Proceed to remove ' + path_)
        input()

        if not os.path.exists(path_):
            print(path_ + ' is already gone')
            return

        try:
            os.rmdir(path_)
            return
        except:
            pass


def run_with_path(path_: str, fn: Callable[[str], None]) -> None:
    mkdir(path_)

    try:
        fn(path_)
    finally:
        remove(path_)
