import codecs
from .constants import *


def load_def_file(file_path):
    with codecs.open(file_path, 'r', 'utf-8-sig') as file:
        result = {}

        cur_line = 0
        for line in file.readlines():
            if line[-1] == '\n':
                line = line[:-1]

            if cur_line == 0:
                result[HASH_KEY] = line

            elif cur_line == 1:
                result[MTIME_KEY] = float(line)
                return result

            else:
                raise Exception()

            cur_line += 1

        raise Exception()


def save_def_file(file_path, hash_, mtime):
    with codecs.open(file_path, 'w', 'utf-8-sig') as file:
        file.write(hash_)
        file.write('\n')

        file.write(str(mtime))
        file.write('\n')
