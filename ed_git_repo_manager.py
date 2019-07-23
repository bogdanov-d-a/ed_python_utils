import argparse
import datetime
import os
import ed_git_repo_userdata
import ed_host_alias
import ed_path_manager
import ed_git_tools
import ed_user_interaction
import ed_pause_at_end
import ed_git_repo_data
import ed_storage_path_data
import ed_host_python_path
import ed_user_password_provider
import ed_file_encryptor


class Data:
    def __init__(self, path, remotes, branches, bundle_versions):
        self.path = path
        self.remotes = remotes
        self.branches = branches
        self.bundle_versions = bundle_versions


def get_host_repos(filter_repos):
    host = ed_host_alias.get()
    result = {}

    repos = ed_git_repo_userdata.get().items()
    if filter_repos is not None:
        repos = filter(lambda elem: elem[0] in filter_repos, repos)

    for repo_alias, repo in repos:
        path_alias = repo.host_to_path.get(host)
        if path_alias is not None:
            path = ed_path_manager.get_host_data().get(path_alias)

            storage_remotes = {}
            for storage_alias, storage_path_alias in repo.remotes.storage.items():
                storage_data = ed_path_manager.get_storage_data_auto(storage_alias)
                if storage_data is not None:
                    storage_path = storage_data.get(storage_path_alias)
                    if storage_path is not None:
                        storage_remotes[storage_alias] = storage_path

            result[repo_alias] = Data(path,
                ed_git_repo_data.Remotes(repo.remotes.native, storage_remotes),
                repo.branches, repo.bundle_versions)

    return result


def host_repos_run(command, filter_repos):
    for repo_alias, repo in get_host_repos(filter_repos).items():
        print(repo_alias)
        command(repo_alias, repo)
        print()
        print()


def host_repos_run_with_path(command, filter_repos):
    host_repos_run(lambda _, repo: command(repo.path), filter_repos)


def host_repos_status(filter_repos):
    host_repos_run_with_path(ed_git_tools.status, filter_repos)

def host_repos_fetch(filter_repos):
    host_repos_run_with_path(ed_git_tools.fetch, filter_repos)

def host_repos_all_refs(filter_repos):
    host_repos_run_with_path(ed_git_tools.all_refs, filter_repos)

def host_repos_all_stash(filter_repos):
    host_repos_run_with_path(ed_git_tools.all_stash, filter_repos)

def host_repos_all_create_bundle(filter_repos):
    target_aliases = set([])
    for repo_alias, repo in get_host_repos(filter_repos).items():
        for target_alias in repo.bundle_versions.keys():
            target_aliases.add(target_alias)
    target_aliases = sorted(target_aliases)

    target_alias = target_aliases[ed_user_interaction.pick_option('Pick target', target_aliases)]

    bundle_path = ed_git_repo_userdata.get_bundle_path()
    if os.path.exists(bundle_path):
        raise Exception(bundle_path + ' exists')
    os.mkdir(bundle_path)

    password = ed_user_password_provider.get()

    def create_bundle(repo_alias, repo):
        last_hash = repo.bundle_versions.get(target_alias)
        if last_hash is not None:
            last_hash_or_root = 'root' if last_hash == '' else last_hash
            now_hash = ed_git_tools.rev_parse(repo.path, 'HEAD')
            if last_hash == now_hash:
                print('No changes found: HEAD is ' + last_hash)
            else:
                print('Updating {0}..{1}'.format(last_hash_or_root, now_hash))
                if last_hash == '':
                    refs = 'HEAD'
                else:
                    refs = last_hash + '..' + 'HEAD'
                bundle_file_path = bundle_path + '\\' + target_alias + '-' + repo_alias + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.bundle'
                ed_git_tools.create_bundle(
                    repo.path,
                    bundle_file_path,
                    refs)
                ed_file_encryptor.encrypt(bundle_file_path, password, bundle_file_path + '.7z')
        else:
            print('No {0} bundle provided'.format(target_alias))
    host_repos_run(create_bundle, filter_repos)

def host_repos_fsck(filter_repos):
    host_repos_run_with_path(ed_git_tools.fsck, filter_repos)

def host_repos_gc(filter_repos):
    host_repos_run_with_path(ed_git_tools.gc, filter_repos)

def handle_all_storage(repo, handler):
    for alias, storage_path in repo.remotes.storage.items():
        print('Processing ' + alias)
        handler(storage_path)

def host_repos_fetch_storage(filter_repos):
    def fetch_all_storage(_, repo):
        handle_all_storage(repo, lambda path: ed_git_tools.fetch_remote(repo.path, path))
    host_repos_run(fetch_all_storage, filter_repos)

def host_repos_pull_storage(filter_repos):
    def pull_all_storage(_, repo):
        handle_all_storage(repo, lambda path: ed_git_tools.pull_with_checkout_multi(repo.path, path, repo.branches))
    host_repos_run(pull_all_storage, filter_repos)

def host_repos_push_storage(filter_repos):
    def push_all_storage(_, repo):
        handle_all_storage(repo, lambda path: ed_git_tools.push_all(repo.path, path))
    host_repos_run(push_all_storage, filter_repos)

def host_repos_fsck_storage(filter_repos):
    def fsck_all_storage(_, repo):
        handle_all_storage(repo, lambda path: ed_git_tools.fsck(path))
    host_repos_run(fsck_all_storage, filter_repos)

def host_repos_pull_native(filter_repos):
    def pull_repo_native(_, repo):
        for remote in repo.remotes.native:
            ed_git_tools.fetch_merge_with_checkout_multi(repo.path, remote, repo.branches)
    host_repos_run(pull_repo_native, filter_repos)

def host_repos_push_native(filter_repos):
    def push_repo_native(_, repo):
        for remote in repo.remotes.native:
            ed_git_tools.push_multi(repo.path, remote, repo.branches)
    host_repos_run(push_repo_native, filter_repos)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action')
    parser.add_argument('--bootstrap', action='store_true')
    args = parser.parse_args()

    if args.action is not None:
        print('action == ' + args.action)
        print('bootstrap == ' + str(args.bootstrap))
        print()

        bootstrap_mode_filter = lambda: ed_git_repo_userdata.bootstrap_repos() if args.bootstrap else None
        if args.action == 'status_all':
            host_repos_status(bootstrap_mode_filter())
        elif args.action == 'ref_status_all':
            host_repos_all_refs(bootstrap_mode_filter())
        elif args.action == 'fetch_all':
            host_repos_fetch(bootstrap_mode_filter())
        elif args.action == 'fetch_storage_all':
            host_repos_fetch_storage(bootstrap_mode_filter())
        elif args.action == 'pull_storage_all':
            host_repos_pull_storage(bootstrap_mode_filter())
        elif args.action == 'push_storage_all':
            host_repos_push_storage(bootstrap_mode_filter())
        elif args.action == 'run_fsck_storage_all':
            host_repos_fsck_storage(bootstrap_mode_filter())
        elif args.action == 'run_fsck_all':
            host_repos_fsck(bootstrap_mode_filter())
        elif args.action == 'gc_all':
            host_repos_gc(bootstrap_mode_filter())
        elif args.action == 'stash_all':
            host_repos_all_stash(bootstrap_mode_filter())
        elif args.action == 'create_bundle_all':
            host_repos_all_create_bundle(bootstrap_mode_filter())
        elif args.action == 'pull_native_all':
            host_repos_pull_native(bootstrap_mode_filter())
        elif args.action == 'push_native_all':
            filter_ = ed_git_repo_userdata.autopush_repos()
            if args.bootstrap:
                filter_ &= bootstrap_mode_filter()
            host_repos_push_native(filter_)
        else:
            raise Exception('unexpected action ' + args.action)
    else:
        bootstrap_mode = False

        while True:
            action = ed_user_interaction.pick_option('Pick action', [
                'Status all',
                'Ref status all',
                'Fetch all',
                'Fetch storage all',
                'Pull storage all',
                'Push storage all',
                'Run fsck storage all',
                'Run fsck all',
                'Run gc all',
                'Stash all',
                'Create bundle all',
                'Pull native all',
                'Push native all',
                'Flip bootstrap_mode',
            ])

            def run_action(action_str):
                python_dir = ed_host_python_path.get_python_3_path()
                if python_dir is None:
                    raise Exception('python3 not found')
                os.system("start " + python_dir + "python.exe ed_git_repo_manager.py --action " + action_str + (' --bootstrap' if bootstrap_mode else ''))

            if action == 0:
                run_action('status_all')
            elif action == 1:
                run_action('ref_status_all')
            elif action == 2:
                run_action('fetch_all')
            elif action == 3:
                run_action('fetch_storage_all')
            elif action == 4:
                run_action('pull_storage_all')
            elif action == 5:
                run_action('push_storage_all')
            elif action == 6:
                run_action('run_fsck_storage_all')
            elif action == 7:
                run_action('run_fsck_all')
            elif action == 8:
                run_action('gc_all')
            elif action == 9:
                run_action('stash_all')
            elif action == 10:
                run_action('create_bundle_all')
            elif action == 11:
                run_action('pull_native_all')
            elif action == 12:
                run_action('push_native_all')
            elif action == 13:
                bootstrap_mode = not bootstrap_mode
                print('bootstrap_mode == ' + str(bootstrap_mode))
            else:
                raise Exception('unexpected action')


if __name__ == '__main__':
    ed_pause_at_end.run(main, 'Program finished successfully')
