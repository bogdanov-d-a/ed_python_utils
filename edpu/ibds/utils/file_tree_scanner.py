def scan(root_path: str, skip_paths: list[str]) -> list[list[str]]:
    from ...file_tree_walker import walk, TYPE_DIR, TYPE_FILE
    from .utils import path_needs_skip

    return walk(
        root_path,
        lambda type, path: type == TYPE_DIR or path_needs_skip(path, skip_paths)
    )[TYPE_FILE]
