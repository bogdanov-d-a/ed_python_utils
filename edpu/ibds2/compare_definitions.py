from .walkers import *


def same_defs(path_a, path_b):
    return walk_def(path_a) == walk_def(path_b)
