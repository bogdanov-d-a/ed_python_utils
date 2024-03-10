from ...utils.data import Data
from typing import Optional


def apply_user_bundle(bundle_path: str, repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ...utils.utils import Data_, host_repos_run
    from os.path import exists

    if not exists(bundle_path):
        raise Exception(bundle_path + ' doesn\'t exist')

    def apply_user_bundle(repo_alias: str, repo: Data_) -> None:
        from os.path import sep

        bundle_file_path = bundle_path + sep + repo_alias + '.bundle'

        if exists(bundle_file_path):
            from ...utils.git import pull_remote
            print('Applying bundle')
            pull_remote(repo.path, bundle_file_path)

        else:
            print('No {0} bundle provided'.format(repo_alias))

    host_repos_run(apply_user_bundle, repos, filter_repos)
