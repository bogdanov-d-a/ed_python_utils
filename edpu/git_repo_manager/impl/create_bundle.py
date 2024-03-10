from ..utils.data import Data
from typing import Callable, Optional


def create_bundle(bundle_hash_path_provider: Callable[[str, str], str], bundle_path: str, bundle_block_reasons: dict[str, str], repos: dict[str, Data], filter_repos: Optional[set[str]]) -> None:
    def get_target_aliases() -> list[str]:
        from ..utils.utils import get_host_repos

        result = set()

        for repo in get_host_repos(repos, filter_repos).values():
            for target_alias in repo.bundles:
                result.add(target_alias)

        return sorted(result)

    def main() -> None:
        from ...guided_directory_use import PathKeeper

        with PathKeeper(bundle_path):
            from ...user_interaction import pick_option
            from ..utils.utils import Data_, host_repos_run
            from edpu_user import password_provider

            target_aliases = get_target_aliases()
            target_alias = target_aliases[pick_option('Pick target', target_aliases)]

            if target_alias in bundle_block_reasons:
                raise Exception(target_alias + ' blocked, reason ' + bundle_block_reasons[target_alias])

            password = password_provider.get()

            def create_bundle_(repo_alias: str, repo: Data_) -> None:
                if target_alias in repo.bundles:
                    from ..utils.bundle import load_line
                    from ..utils.git import rev_parse

                    hash_file_path = bundle_hash_path_provider(target_alias, repo_alias)
                    last_hash = load_line(hash_file_path)
                    last_hash_or_root = 'root' if last_hash is None else last_hash
                    now_hash = rev_parse(repo.path, 'HEAD')
    
                    if last_hash == now_hash:
                        print('No changes found: HEAD is ' + str(last_hash))

                    else:
                        from ...datetime_utils import get_now_datetime_str
                        from ...file_encryptor import encrypt
                        from ..utils.bundle import save_line
                        from ..utils.git import create_bundle as impl
                        from os.path import sep

                        print('Updating {0}..{1}'.format(last_hash_or_root, now_hash))

                        if last_hash is None:
                            refs = 'HEAD'
                        else:
                            refs = last_hash + '..' + 'HEAD'

                        bundle_file_path = bundle_path + sep + target_alias + '-' + repo_alias + '-' + get_now_datetime_str() + '.bundle'

                        impl(repo.path, bundle_file_path, refs)
                        encrypt(bundle_file_path, password, bundle_file_path + '.7z')
                        save_line(now_hash, hash_file_path)

                else:
                    print('No {0} bundle provided'.format(target_alias))

            host_repos_run(create_bundle_, repos, filter_repos)

    main()
