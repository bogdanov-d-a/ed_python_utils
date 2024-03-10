from ...utils.data import Data
from typing import Optional


def get_user_bundle_info(user_bundle_info_path: str, repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ...utils.utils import Data_, host_repos_run
    from codecs import open

    result: list[str] = []

    def get_user_bundle_info(repo_alias: str, repo: Data_) -> None:
        from ...utils.git import rev_parse

        now_hash = rev_parse(repo.path, 'HEAD')

        nonlocal result
        result.append(now_hash + ' ' + repo_alias)

    host_repos_run(get_user_bundle_info, repos, filter_repos, False)

    with open(user_bundle_info_path, 'w', 'utf-8') as f:
        f.write('|'.join(result))
