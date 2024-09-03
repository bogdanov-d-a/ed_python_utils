from __future__ import annotations
from typing import Optional


class WorktreeData:
    def __init__(self: WorktreeData, path: str, alias: str) -> None:
        self.path = path
        self.alias = alias


def add_worktree(path: str, worktree_path: str, revision: str) -> None:
    from .utils.git import worktree_add_detach
    worktree_add_detach(path, worktree_path, revision)


def discard_worktree(path: str, branch: str, worktree: Optional[WorktreeData]) -> None:
    from .utils.git import checkout, clean_ffdx

    data_path = path if worktree is None else worktree.path
    checkout(data_path, branch, True)

    def remove_index() -> None:
        from os.path import isfile
        index_path = fr'{path}\.git' + ('' if worktree is None else fr'\worktrees\{worktree.alias}') + r'\index'

        if isfile(index_path):
            from os import remove
            remove(index_path)
        else:
            print(f'not isfile({index_path})')

    remove_index()

    clean_ffdx(data_path)
