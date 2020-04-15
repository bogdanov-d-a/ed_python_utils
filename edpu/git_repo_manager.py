import argparse
import datetime
import os
import edpu_user.git_repo_data
import edpu.host_alias
import edpu.path_manager
import edpu.git_tools
import edpu.user_interaction
import edpu.pause_at_end
import edpu.git_repo_data
import edpu_user.python_launcher
import edpu_user.password_provider
import edpu.file_encryptor
import edpu.datetime_utils


class Data:
    def __init__(self, path, remotes, branches, bundles):
        self.path = path
        self.remotes = remotes
        self.branches = branches
        self.bundles = bundles


def get_host_repos(filter_repos):
    host = edpu.host_alias.get()
    result = {}

    repos = edpu_user.git_repo_data.get().items()
    if filter_repos is not None:
        repos = filter(lambda elem: elem[0] in filter_repos, repos)

    for repo_alias, repo in repos:
        path_alias = repo.host_to_path.get(host)
        if path_alias is not None:
            path = edpu.path_manager.get_host_data().get(path_alias)

            storage_remotes = {}
            for storage_alias, storage_path_alias in repo.remotes.storage.items():
                storage_data = edpu.path_manager.get_storage_data_auto(storage_alias)
                if storage_data is not None:
                    storage_path = storage_data.get(storage_path_alias)
                    if storage_path is not None:
                        storage_remotes[storage_alias] = storage_path

            result[repo_alias] = Data(path,
                edpu.git_repo_data.Remotes(repo.remotes.native, storage_remotes),
                repo.branches, repo.bundles)

    return result


def host_repos_run(command, filter_repos):
    for repo_alias, repo in get_host_repos(filter_repos).items():
        print(repo_alias)
        command(repo_alias, repo)
        print()
        print()


def host_repos_run_with_path(command, filter_repos):
    host_repos_run(lambda _, repo: command(repo.path), filter_repos)


def run_with_bundle_path(f):
    bundle_path = edpu_user.git_repo_data.get_bundle_path()
    if os.path.exists(bundle_path):
        raise Exception(bundle_path + ' exists')
    os.mkdir(bundle_path)

    try:
        f(bundle_path)
    finally:
        try:
            os.rmdir(bundle_path)
        except:
            pass


def host_repos_status(filter_repos):
    host_repos_run_with_path(edpu.git_tools.status, filter_repos)

def host_repos_fetch(filter_repos):
    host_repos_run_with_path(edpu.git_tools.fetch, filter_repos)

def host_repos_all_refs(filter_repos):
    host_repos_run_with_path(edpu.git_tools.all_refs, filter_repos)

def host_repos_all_stash(filter_repos):
    host_repos_run_with_path(edpu.git_tools.all_stash, filter_repos)

def host_repos_all_create_bundle(filter_repos):
    def bundle_path_callback(bundle_path):
        target_aliases = set([])
        for _, repo in get_host_repos(filter_repos).items():
            for target_alias in repo.bundles:
                target_aliases.add(target_alias)
        target_aliases = sorted(target_aliases)

        target_alias = target_aliases[edpu.user_interaction.pick_option('Pick target', target_aliases)]
        password = edpu_user.password_provider.get()

        def create_bundle(repo_alias, repo):
            def load_line(path):
                if not os.path.exists(path):
                    return None
                with open(path) as f:
                    return f.readlines()[0].rstrip('\n')

            def save_line(line, path):
                with open(path, 'w') as f:
                    f.write(line)

            if target_alias in repo.bundles:
                hash_file_path = edpu_user.git_repo_data.get_bundle_hash_path(target_alias, repo_alias)
                last_hash = load_line(hash_file_path)
                last_hash_or_root = 'root' if last_hash is None else last_hash
                now_hash = edpu.git_tools.rev_parse(repo.path, 'HEAD')
                if last_hash == now_hash:
                    print('No changes found: HEAD is ' + last_hash)
                else:
                    print('Updating {0}..{1}'.format(last_hash_or_root, now_hash))
                    if last_hash is None:
                        refs = 'HEAD'
                    else:
                        refs = last_hash + '..' + 'HEAD'
                    bundle_file_path = bundle_path + '\\' + target_alias + '-' + repo_alias + '-' + edpu.datetime_utils.get_now_datetime_str() + '.bundle'
                    edpu.git_tools.create_bundle(
                        repo.path,
                        bundle_file_path,
                        refs)
                    edpu.file_encryptor.encrypt(bundle_file_path, password, bundle_file_path + '.7z')
                    save_line(now_hash, hash_file_path)
            else:
                print('No {0} bundle provided'.format(target_alias))

        host_repos_run(create_bundle, filter_repos)

    run_with_bundle_path(bundle_path_callback)

def host_repos_all_get_user_bundle_info(filter_repos):
    def get_user_bundle_info(repo_alias, repo):
        now_hash = edpu.git_tools.rev_parse(repo.path, 'HEAD')
        print(repo_alias + ' ' + now_hash)

    host_repos_run(get_user_bundle_info, filter_repos)

def host_repos_all_create_user_bundle(filter_repos):
    pass

def host_repos_all_apply_user_bundle(filter_repos):
    pass

def host_repos_fsck(filter_repos):
    host_repos_run_with_path(edpu.git_tools.fsck, filter_repos)

def host_repos_gc(filter_repos):
    host_repos_run_with_path(edpu.git_tools.gc, filter_repos)

def handle_all_storage(repo, handler):
    for alias, storage_path in repo.remotes.storage.items():
        print('Processing ' + alias)
        handler(storage_path)

def host_repos_fetch_storage(filter_repos):
    def fetch_all_storage(_, repo):
        handle_all_storage(repo, lambda path: edpu.git_tools.fetch_remote(repo.path, path))
    host_repos_run(fetch_all_storage, filter_repos)

def host_repos_pull_storage(filter_repos):
    def pull_all_storage(_, repo):
        handle_all_storage(repo, lambda path: edpu.git_tools.pull_with_checkout_multi(repo.path, path, repo.branches))
    host_repos_run(pull_all_storage, filter_repos)

def host_repos_push_storage(filter_repos):
    def push_all_storage(_, repo):
        handle_all_storage(repo, lambda path: edpu.git_tools.push_all(repo.path, path))
    host_repos_run(push_all_storage, filter_repos)

def host_repos_fsck_storage(filter_repos):
    def fsck_all_storage(_, repo):
        handle_all_storage(repo, lambda path: edpu.git_tools.fsck(path))
    host_repos_run(fsck_all_storage, filter_repos)

def host_repos_pull_native(filter_repos):
    def pull_repo_native(_, repo):
        for remote in repo.remotes.native:
            edpu.git_tools.fetch_merge_with_checkout_multi(repo.path, remote, repo.branches)
    host_repos_run(pull_repo_native, filter_repos)

def host_repos_push_native(filter_repos):
    def push_repo_native(_, repo):
        for remote in repo.remotes.native:
            edpu.git_tools.push_multi(repo.path, remote, repo.branches)
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

        bootstrap_mode_filter = lambda: edpu_user.git_repo_data.bootstrap_repos() if args.bootstrap else None
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
        elif args.action == 'get_user_bundle_info':
            host_repos_all_get_user_bundle_info(bootstrap_mode_filter())
        elif args.action == 'create_user_bundle':
            host_repos_all_create_user_bundle(bootstrap_mode_filter())
        elif args.action == 'apply_user_bundle':
            host_repos_all_apply_user_bundle(bootstrap_mode_filter())
        elif args.action == 'pull_native_all':
            host_repos_pull_native(bootstrap_mode_filter())
        elif args.action == 'push_native_all':
            filter_ = edpu_user.git_repo_data.autopush_repos()
            if args.bootstrap:
                filter_ &= bootstrap_mode_filter()
            host_repos_push_native(filter_)
        else:
            raise Exception('unexpected action ' + args.action)
    else:
        bootstrap_mode = False

        while True:
            action = edpu.user_interaction.pick_option('Pick action', [
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
                'Get user bundle info',
                'Create user bundle',
                'Apply user bundle',
                'Pull native all',
                'Push native all',
                'Flip bootstrap_mode',
            ])

            def run_action(action_str):
                edpu_user.python_launcher.start_with_python3('git_repo_manager.py --action ' + action_str + (' --bootstrap' if bootstrap_mode else ''), '.')

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
                run_action('get_user_bundle_info')
            elif action == 12:
                run_action('create_user_bundle')
            elif action == 13:
                run_action('apply_user_bundle')
            elif action == 14:
                run_action('pull_native_all')
            elif action == 15:
                run_action('push_native_all')
            elif action == 16:
                bootstrap_mode = not bootstrap_mode
                print('bootstrap_mode == ' + str(bootstrap_mode))
            else:
                raise Exception('unexpected action')


if __name__ == '__main__':
    edpu.pause_at_end.run(main, 'Program finished successfully')
