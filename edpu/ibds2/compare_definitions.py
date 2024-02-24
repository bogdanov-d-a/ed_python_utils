from .walkers import walk_def
from concurrent.futures import ProcessPoolExecutor


def same_defs(path_a: str, path_b: str) -> bool:
    with ProcessPoolExecutor(2) as executor:
        results = list(executor.map(walk_def, [path_a, path_b]))

    return results[0] == results[1]
