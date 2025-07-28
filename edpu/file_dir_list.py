from typing import Any, Callable


def file_dir_list(
    root: str,
    file_path: str,
    dir_path: str,
    ignore_callback: Callable[[str, list[str]], bool]=lambda *_: False
) -> None:
    with open(file_path, 'w', encoding='utf-8') as file_file:
        with open(dir_path, 'w', encoding='utf-8') as dir_file:
            from .file_tree_walker import walk, TYPE_FILE, TYPE_DIR
            from os import sep

            walk_result = walk(root, ignore_callback)

            for path in sorted(map(
                lambda path: sep.join(path),
                walk_result[TYPE_FILE]
            )):
                file_file.write(path + '\n')

            for path in sorted(map(
                lambda path: sep.join(path),
                walk_result[TYPE_DIR]
            )):
                dir_file.write(path + '\n')


def get_ignored_paths_tries(ignored_paths: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    from .trie import make_trie

    ignored_paths_dir = list(map(
        lambda path: path[:-1],
        filter(
            lambda path: path.endswith('\\'),
            ignored_paths
        )
    ))

    return (
        make_trie(ignored_paths),
        make_trie(ignored_paths_dir)
    )


def get_ignore_callback(trie: dict[str, Any], trie_dir: dict[str, Any]) -> Callable[[str, list[str]], bool]:
    def ignore_callback(type: str, path: list[str]) -> bool:
        from .file_tree_walker import TYPE_DIR
        from .trie import in_trie
        from os import sep

        path_ = sep.join(path)

        if type == TYPE_DIR and in_trie(trie_dir, path_):
            return True

        return in_trie(trie, path_, True)

    return ignore_callback
