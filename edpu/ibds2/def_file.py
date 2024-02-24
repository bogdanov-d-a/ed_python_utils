from __future__ import annotations
import codecs
from .constants import *


class DefFileData:
    def __init__(self: DefFileData, hash_: str, mtime: float) -> None:
        self.hash_ = hash_
        self.mtime = mtime


def load_def_file(file_path: str) -> DefFileData:
    with codecs.open(file_path, 'r', 'utf-8-sig') as file:
        cur_line = 0
        for line in file.readlines():
            if line[-1] == '\n':
                line = line[:-1]

            if cur_line == 0:
                hash_ = line

            elif cur_line == 1:
                mtime = float(line)
                return DefFileData(hash_, mtime)

            else:
                raise Exception()

            cur_line += 1

        raise Exception()


def save_def_file(file_path: str, data: DefFileData) -> None:
    with codecs.open(file_path, 'w', 'utf-8-sig') as file:
        file.write(data.hash_)
        file.write('\n')

        file.write(str(data.mtime))
        file.write('\n')
