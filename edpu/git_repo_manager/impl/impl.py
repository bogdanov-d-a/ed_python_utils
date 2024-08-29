from ..utils.data import Data
from typing import Optional


def host_repos_status(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.git import status
    from ..utils.utils import host_repos_run_with_path

    host_repos_run_with_path(status, repos, filter_repos)


def host_repos_remotes(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.git import remotes
    from ..utils.utils import host_repos_run_with_path

    host_repos_run_with_path(remotes, repos, filter_repos)


def host_repos_fetch(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.git import fetch
    from ..utils.utils import host_repos_run_with_path

    host_repos_run_with_path(fetch, repos, filter_repos)


def host_repos_all_refs(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.git import all_refs
    from ..utils.utils import host_repos_run_with_path

    host_repos_run_with_path(all_refs, repos, filter_repos)


def host_repos_all_storage_refs(repos: dict[str, Data], storage_block_reasons: dict[str, str], filter_repos: Optional[set[str]]) -> None:
    from ..utils.utils import Data_, host_repos_run

    def ref_all_storage(_, repo: Data_) -> None:
        from ..utils.git import all_refs
        from ..utils.utils import handle_all_storage

        handle_all_storage(repo, storage_block_reasons, all_refs)

    host_repos_run(ref_all_storage, repos, filter_repos)


def host_repos_all_stash(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.git import all_stash
    from ..utils.utils import host_repos_run_with_path

    host_repos_run_with_path(all_stash, repos, filter_repos)


def host_repos_fsck(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.git import fsck
    from ..utils.utils import host_repos_run_with_path

    host_repos_run_with_path(fsck, repos, filter_repos)


def host_repos_gc(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.git import gc
    from ..utils.utils import host_repos_run_with_path

    host_repos_run_with_path(gc, repos, filter_repos)


def host_repos_fetch_storage(repos: dict[str, Data], storage_block_reasons: dict[str, str], filter_repos: Optional[set[str]]) -> None:
    from ..utils.utils import Data_, host_repos_run

    def fetch_all_storage(_, repo: Data_) -> None:
        from ..utils.git import fetch_remote
        from ..utils.utils import handle_all_storage

        handle_all_storage(repo, storage_block_reasons, lambda path: fetch_remote(repo.path, path))

    host_repos_run(fetch_all_storage, repos, filter_repos)


def host_repos_pull_storage(repos: dict[str, Data], storage_block_reasons: dict[str, str], filter_repos: Optional[set[str]]) -> None:
    from ..utils.utils import Data_, host_repos_run

    def pull_all_storage(_, repo: Data_) -> None:
        from ..utils.utils import handle_all_storage

        def pull_storage(path: str) -> None:
            from ..utils.git import pull_with_checkout_multi
            from ..utils.utils import init_if_not_exists

            init_if_not_exists(repo.path)
            pull_with_checkout_multi(repo.path, path, repo.branches)

        handle_all_storage(repo, storage_block_reasons, pull_storage)

    host_repos_run(pull_all_storage, repos, filter_repos)


def host_repos_push_storage(repos: dict[str, Data], storage_block_reasons: dict[str, str], filter_repos: Optional[set[str]]) -> None:
    from ..utils.utils import Data_, host_repos_run

    def push_all_storage(_, repo: Data_) -> None:
        from ..utils.utils import handle_all_storage

        def push_storage(path: str) -> None:
            from ..utils.git import push_all
            from ..utils.utils import init_bare_if_not_exists

            init_bare_if_not_exists(path)
            push_all(repo.path, path)

        handle_all_storage(repo, storage_block_reasons, push_storage)

    host_repos_run(push_all_storage, repos, filter_repos)


def host_repos_fsck_storage(repos: dict[str, Data], storage_block_reasons: dict[str, str], filter_repos: Optional[set[str]]) -> None:
    from ..utils.utils import Data_, host_repos_run

    def fsck_all_storage(_, repo: Data_) -> None:
        from ..utils.git import fsck
        from ..utils.utils import handle_all_storage

        handle_all_storage(repo, storage_block_reasons, fsck)

    host_repos_run(fsck_all_storage, repos, filter_repos)


def host_repos_pull_native(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.utils import Data_, host_repos_run

    def pull_repo_native(_, repo: Data_) -> None:
        for remote in repo.remotes.native:
            from ..utils.git import fetch_merge_with_checkout_multi
            fetch_merge_with_checkout_multi(repo.path, remote, repo.branches)

    host_repos_run(pull_repo_native, repos, filter_repos)


def host_repos_push_native(repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ..utils.utils import Data_, host_repos_run

    def push_repo_native(_, repo: Data_) -> None:
        for remote in repo.remotes.native:
            from ..utils.git import push_multi
            push_multi(repo.path, remote, repo.branches)

    host_repos_run(push_repo_native, repos, filter_repos)
