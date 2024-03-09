from .. import file_tree_walker
from . import ibds_utils


def scan(root_path: str, skip_paths: list[str]) -> list[list[str]]:
    return file_tree_walker.walk(
        root_path,
        lambda type, path: type == file_tree_walker.TYPE_DIR or ibds_utils.path_needs_skip(path, skip_paths)
    )[file_tree_walker.TYPE_FILE]
