from __future__ import annotations
from .data import Data, Remotes
from typing import Callable, Optional


class Data_:
    def __init__(self: Data_, path: str, remotes: Remotes, branches: list[str], bundles: list[str]) -> None:
        self.path = path
        self.remotes = remotes
        self.branches = branches
        self.bundles = bundles


def get_host_repos(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> dict[str, Data_]:
    from ... import host_alias
    from ...storage_finder import find_all_storage

    host = host_alias.get()
    result: dict[str, Data_] = {}

    repos_items = repos.items()

    if filter_repos is not None:
        repos_items = filter(lambda repos_item: repos_item[0] in filter_repos, repos_items)

    all_storage = find_all_storage()

    for repo_alias, repo in repos_items:
        path = repo.host_to_path.get(host)

        if path is None:
            continue

        storage_remotes: dict[str, str] = {}

        for storage_alias, storage_path in repo.remotes.storage.items():
            storage_root = all_storage.get(storage_alias)

            if storage_root is not None:
                storage_remotes[storage_alias] = storage_root + storage_path

        result[repo_alias] = Data_(
            path,
            Remotes(repo.remotes.native, storage_remotes),
            repo.branches,
            repo.bundles
        )

    return result


def host_repos_run(command: Callable[[str, Data_], None], repos: dict[str, Data], filter_repos: Optional[set[str]], show_annotations: bool=True) -> None:
    for repo_alias, repo in get_host_repos(repos, filter_repos).items():
        if show_annotations:
            print(repo_alias)

        command(repo_alias, repo)

        if show_annotations:
            print()
            print()


def host_repos_run_with_path(command: Callable[[str], None], repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    host_repos_run(lambda _, repo: command(repo.path), repos, filter_repos)


def handle_all_storage(repo: Data_, block_reasons: dict[str, str], handler: Callable[[str], None]) -> None:
    for alias, storage_path in repo.remotes.storage.items():
        if alias in block_reasons:
            raise Exception(alias + ' blocked, reason ' + block_reasons[alias])

        print('Processing ' + alias)
        handler(storage_path)


class Args:
    def __init__(self: Args, action: str, bootstrap: bool) -> None:
        self.action = action
        self.bootstrap = bootstrap

    def build_cmd(self: Args, filename: str) -> str:
        from ...string_utils import merge_with_space, quotation_mark_wrap

        data = [
            quotation_mark_wrap(filename),
            '--action',
            self.action,
        ]

        if self.bootstrap:
            data.append('--bootstrap')

        return merge_with_space(data)

    @staticmethod
    def parse() -> Optional[Args]:
        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument('--action')
        parser.add_argument('--bootstrap', action='store_true')
        args = parser.parse_args()

        if not args.action:
            return None

        return Args(args.action, args.bootstrap)


def init_bare_if_not_exists(path: str) -> None:
    from os.path import isdir

    if isdir(path):
        return

    from os.path import split
    parent_path = split(path)[0]

    if not isdir(parent_path):
        raise Exception(parent_path + ' doesn\'t exist')

    print(path + ' is missing, creating')

    from os import makedirs
    makedirs(path)

    from .git import init_bare
    init_bare(path)
