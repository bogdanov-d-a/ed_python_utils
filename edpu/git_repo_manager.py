import argparse
import codecs
import operator
import os
from edpu import host_alias
from edpu import git_tools
from edpu import user_interaction
from edpu import pause_at_end
from edpu import git_repo_data
import edpu_user.python_launcher
import edpu_user.password_provider
from edpu import file_encryptor
from edpu import datetime_utils
from edpu.storage_finder import find_all_storage


class Data:
    def __init__(self, path, remotes, branches, bundles):
        self.path = path
        self.remotes = remotes
        self.branches = branches
        self.bundles = bundles


def get_host_repos(repos, filter_repos):
    host = host_alias.get()
    result = {}

    repos_items = repos.items()
    if filter_repos is not None:
        repos_items = filter(lambda elem: elem[0] in filter_repos, repos_items)

    all_storage = find_all_storage()

    for repo_alias, repo in repos_items:
        path = repo.host_to_path.get(host)
        if path is None:
            continue

        storage_remotes = {}
        for storage_alias, storage_path in repo.remotes.storage.items():
            storage_root = all_storage.get(storage_alias)
            if storage_root is not None:
                storage_remotes[storage_alias] = storage_root + storage_path

        result[repo_alias] = Data(path,
            git_repo_data.Remotes(repo.remotes.native, storage_remotes),
            repo.branches, repo.bundles)

    return result


def host_repos_run(command, repos, filter_repos, show_annotations=True):
    for repo_alias, repo in get_host_repos(repos, filter_repos).items():
        if show_annotations:
            print(repo_alias)
        command(repo_alias, repo)
        if show_annotations:
            print()
            print()


def host_repos_run_with_path(command, repos, filter_repos):
    host_repos_run(lambda _, repo: command(repo.path), repos, filter_repos)


def run_with_bundle_path(bundle_path, f):
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


def host_repos_status(repos, filter_repos):
    host_repos_run_with_path(git_tools.status, repos, filter_repos)

def host_repos_remotes(repos, filter_repos):
    host_repos_run_with_path(git_tools.remotes, repos, filter_repos)

def host_repos_fetch(repos, filter_repos):
    host_repos_run_with_path(git_tools.fetch, repos, filter_repos)

def host_repos_all_refs(repos, filter_repos):
    host_repos_run_with_path(git_tools.all_refs, repos, filter_repos)

def host_repos_all_storage_refs(repos, filter_repos):
    def ref_all_storage(_, repo):
        handle_all_storage(repo, lambda path: git_tools.all_refs(path))
    host_repos_run(ref_all_storage, repos, filter_repos)

def host_repos_all_stash(repos, filter_repos):
    host_repos_run_with_path(git_tools.all_stash, repos, filter_repos)

def host_repos_all_create_bundle(bundle_hash_path_provider, bundle_path, bundle_block_reasons, repos, filter_repos):
    def bundle_path_callback(bundle_path):
        target_aliases = set([])
        for _, repo in get_host_repos(repos, filter_repos).items():
            for target_alias in repo.bundles:
                target_aliases.add(target_alias)
        target_aliases = sorted(target_aliases)

        target_alias = target_aliases[user_interaction.pick_option('Pick target', target_aliases)]

        if target_alias in bundle_block_reasons:
            raise Exception(target_alias + ' blocked, reason ' + bundle_block_reasons.get(target_alias))

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
                hash_file_path = bundle_hash_path_provider(target_alias, repo_alias)
                last_hash = load_line(hash_file_path)
                last_hash_or_root = 'root' if last_hash is None else last_hash
                now_hash = git_tools.rev_parse(repo.path, 'HEAD')
                if last_hash == now_hash:
                    print('No changes found: HEAD is ' + last_hash)
                else:
                    print('Updating {0}..{1}'.format(last_hash_or_root, now_hash))
                    if last_hash is None:
                        refs = 'HEAD'
                    else:
                        refs = last_hash + '..' + 'HEAD'
                    bundle_file_path = bundle_path + os.path.sep + target_alias + '-' + repo_alias + '-' + datetime_utils.get_now_datetime_str() + '.bundle'
                    git_tools.create_bundle(
                        repo.path,
                        bundle_file_path,
                        refs)
                    file_encryptor.encrypt(bundle_file_path, password, bundle_file_path + '.7z')
                    save_line(now_hash, hash_file_path)
            else:
                print('No {0} bundle provided'.format(target_alias))

        host_repos_run(create_bundle, repos, filter_repos)

    run_with_bundle_path(bundle_path, bundle_path_callback)

def host_repos_all_get_user_bundle_info(user_bundle_info_path, repos, filter_repos):
    result = []

    def get_user_bundle_info(repo_alias, repo):
        nonlocal result
        now_hash = git_tools.rev_parse(repo.path, 'HEAD')
        result.append(now_hash + ' ' + repo_alias)

    host_repos_run(get_user_bundle_info, repos, filter_repos, False)

    with codecs.open(user_bundle_info_path, 'w', 'utf-8') as f:
        f.write('|'.join(result))

def host_repos_all_create_user_bundle(user_bundle_info_new_path, bundle_path, repos, filter_repos):
    def bundle_path_callback(bundle_path):
        user_info = {}
        for line in input().split('|'):
            hash_, alias = line.split(' ', 1)
            user_info[alias] = hash_

        user_info_new = dict(user_info)

        def create_user_bundle(repo_alias, repo):
            user_hash = user_info.get(repo_alias)
            if user_hash is not None:
                now_hash = git_tools.rev_parse(repo.path, 'HEAD')
                if user_hash == now_hash:
                    print('No changes found: HEAD is ' + user_hash)
                else:
                    print('Packing {0}..{1}'.format(user_hash, now_hash))
                    git_tools.create_bundle(
                        repo.path,
                        bundle_path + os.path.sep + repo_alias + '.bundle',
                        user_hash + '..' + 'HEAD')
                    user_info_new[repo_alias] = now_hash
            else:
                print('No {0} bundle requested'.format(repo_alias))

        host_repos_run(create_user_bundle, repos, filter_repos)

        if user_info != user_info_new:
            with codecs.open(user_bundle_info_new_path, 'w', 'utf-8') as f:
                f.write('|'.join(map(lambda e: e[1] + ' ' + e[0], user_info_new.items())))

    run_with_bundle_path(bundle_path, bundle_path_callback)

def host_repos_all_apply_user_bundle(bundle_path, repos, filter_repos):
    if not os.path.exists(bundle_path):
        raise Exception(bundle_path + ' doesn\'t exist')

    def apply_user_bundle(repo_alias, repo):
        bundle_file_path = bundle_path + os.path.sep + repo_alias + '.bundle'
        if os.path.exists(bundle_file_path):
            print('Applying bundle')
            git_tools.pull_remote(
                repo.path,
                bundle_file_path)
        else:
            print('No {0} bundle provided'.format(repo_alias))

    host_repos_run(apply_user_bundle, repos, filter_repos)

def host_repos_fsck(repos, filter_repos):
    host_repos_run_with_path(git_tools.fsck, repos, filter_repos)

def host_repos_gc(repos, filter_repos):
    host_repos_run_with_path(git_tools.gc, repos, filter_repos)

def handle_all_storage(repo, handler):
    for alias, storage_path in repo.remotes.storage.items():
        print('Processing ' + alias)
        handler(storage_path)

def host_repos_fetch_storage(repos, filter_repos):
    def fetch_all_storage(_, repo):
        handle_all_storage(repo, lambda path: git_tools.fetch_remote(repo.path, path))
    host_repos_run(fetch_all_storage, repos, filter_repos)

def host_repos_pull_storage(repos, filter_repos):
    def pull_all_storage(_, repo):
        handle_all_storage(repo, lambda path: git_tools.pull_with_checkout_multi(repo.path, path, repo.branches))
    host_repos_run(pull_all_storage, repos, filter_repos)

def host_repos_push_storage(repos, filter_repos):
    def push_all_storage(_, repo):
        def handler(path):
            if not os.path.isdir(path):
                parent_path = os.path.split(path)[0]
                if not os.path.isdir(parent_path):
                    raise Exception(parent_path + ' doesn\'t exist')
                print(path + ' is missing, creating')
                os.makedirs(path)
                git_tools.init_bare(path)
            git_tools.push_all(repo.path, path)
        handle_all_storage(repo, handler)
    host_repos_run(push_all_storage, repos, filter_repos)

def host_repos_fsck_storage(repos, filter_repos):
    def fsck_all_storage(_, repo):
        handle_all_storage(repo, lambda path: git_tools.fsck(path))
    host_repos_run(fsck_all_storage, repos, filter_repos)

def host_repos_pull_native(repos, filter_repos):
    def pull_repo_native(_, repo):
        for remote in repo.remotes.native:
            git_tools.fetch_merge_with_checkout_multi(repo.path, remote, repo.branches)
    host_repos_run(pull_repo_native, repos, filter_repos)

def host_repos_push_native(repos, filter_repos):
    def push_repo_native(_, repo):
        for remote in repo.remotes.native:
            git_tools.push_multi(repo.path, remote, repo.branches)
    host_repos_run(push_repo_native, repos, filter_repos)


def main(data_provider):
    parser = argparse.ArgumentParser()
    parser.add_argument('--action')
    parser.add_argument('--bootstrap', action='store_true')
    args = parser.parse_args()

    bootstrap_mode_filter = lambda: data_provider.get_bootstrap_repos() if args.bootstrap else None

    def push_native_all_action_handler():
        filter_ = data_provider.get_autopush_repos()
        if args.bootstrap:
            filter_ &= bootstrap_mode_filter()
        host_repos_push_native(data_provider.get_repos(), filter_)

    actions = [
        (
            'status_all',
            'Status',
            lambda: host_repos_status(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'ref_status_all',
            'List refs',
            lambda: host_repos_all_refs(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'ref_status_storage_all',
            'List storage refs',
            lambda: host_repos_all_storage_refs(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'remote_status_all',
            'List remotes',
            lambda: host_repos_remotes(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'stash_all',
            'List stash',
            lambda: host_repos_all_stash(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'fetch_all',
            'Fetch native',
            lambda: host_repos_fetch(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'fetch_storage_all',
            'Fetch storage',
            lambda: host_repos_fetch_storage(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'pull_native_all',
            'Pull native',
            lambda: host_repos_pull_native(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'pull_storage_all',
            'Pull storage',
            lambda: host_repos_pull_storage(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'push_native_all',
            'Push native',
            push_native_all_action_handler
        ),
        (
            'push_storage_all',
            'Push storage',
            lambda: host_repos_push_storage(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'run_fsck_all',
            'Run fsck',
            lambda: host_repos_fsck(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'run_fsck_storage_all',
            'Run fsck storage',
            lambda: host_repos_fsck_storage(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'gc_all',
            'Run gc',
            lambda: host_repos_gc(data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'create_bundle_all',
            'Create bundle',
            lambda: host_repos_all_create_bundle(lambda target_alias, repo_alias: data_provider.get_bundle_hash_path(target_alias, repo_alias), data_provider.get_bundle_path(), data_provider.get_bundle_block_reasons(), data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'get_user_bundle_info',
            'Get user bundle info',
            lambda: host_repos_all_get_user_bundle_info(data_provider.get_user_bundle_info_path(), data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'create_user_bundle',
            'Create user bundle',
            lambda: host_repos_all_create_user_bundle(data_provider.get_user_bundle_info_new_path(), data_provider.get_bundle_path(), data_provider.get_repos(), bootstrap_mode_filter())
        ),
        (
            'apply_user_bundle',
            'Apply user bundle',
            lambda: host_repos_all_apply_user_bundle(data_provider.get_bundle_path(), data_provider.get_repos(), bootstrap_mode_filter())
        ),
    ]

    bootstrap_mode = False

    def flip_bootstrap_mode_action_handler():
        nonlocal bootstrap_mode
        bootstrap_mode = not bootstrap_mode
        print('bootstrap_mode == ' + str(bootstrap_mode))

    actions_in_place = [
        (
            'Flip bootstrap_mode',
            flip_bootstrap_mode_action_handler
        ),
    ]

    if args.action is not None:
        print('action == ' + args.action)
        print('bootstrap == ' + str(args.bootstrap))
        print()

        def find_action_by_id(id):
            for action in actions:
                if action[0] == args.action:
                    return action
            raise Exception('unexpected action ' + id)

        find_action_by_id(args.action)[2]()
    else:
        while True:
            action = user_interaction.pick_option('Pick action', list(map(operator.itemgetter(1), actions)) + list(map(operator.itemgetter(0), actions_in_place)))

            def run_action(action_str):
                edpu_user.python_launcher.start_with_python3('git_repo_manager.py --action ' + action_str + (' --bootstrap' if bootstrap_mode else ''), '.')

            if action < len(actions):
                run_action(actions[action][0])
            elif action - len(actions) < len(actions_in_place):
                actions_in_place[action - len(actions)][1]()
            else:
                raise Exception('unexpected action')


def run(data_provider):
    pause_at_end.run(lambda: main(data_provider), 'Program finished successfully')
