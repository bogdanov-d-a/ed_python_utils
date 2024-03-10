from ...utils.data import Data
from typing import Optional


def _get_user_info() -> dict[str, str]:
    result: dict[str, str] = {}

    for line in input().split('|'):
        hash_, alias = line.split(' ', 1)
        result[alias] = hash_

    return result


def create_user_bundle(user_bundle_info_new_path: str, bundle_path: str, repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    from ....guided_directory_use import PathKeeper

    with PathKeeper(bundle_path):
        from ...utils.utils import Data_, host_repos_run

        user_info = _get_user_info()
        user_info_new = dict(user_info)

        def create_user_bundle(repo_alias: str, repo: Data_) -> None:
            user_hash = user_info.get(repo_alias)

            if user_hash is not None:
                from ...utils.git import rev_parse

                now_hash = rev_parse(repo.path, 'HEAD')

                if user_hash == now_hash:
                    print('No changes found: HEAD is ' + user_hash)

                else:
                    from ...utils.git import create_bundle
                    from os.path import sep

                    print('Packing {0}..{1}'.format(user_hash, now_hash))

                    create_bundle(
                        repo.path,
                        bundle_path + sep + repo_alias + '.bundle',
                        user_hash + '..' + 'HEAD'
                    )

                    user_info_new[repo_alias] = now_hash

            else:
                print('No {0} bundle requested'.format(repo_alias))

        host_repos_run(create_user_bundle, repos, filter_repos)

        if user_info != user_info_new:
            from codecs import open

            with open(user_bundle_info_new_path, 'w', 'utf-8') as f:
                f.write('|'.join(map(lambda e: e[1] + ' ' + e[0], user_info_new.items())))
