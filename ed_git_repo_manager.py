import ed_git_repo_userdata
import ed_host_alias
import ed_path_manager
import ed_git_tools
import ed_user_interaction
import ed_pause_at_end
import ed_storage_finder
import ed_git_repo_data
import ed_storage_path_data


class Data:
    def __init__(self, path, remotes, branches):
        self.path = path
        self.remotes = remotes
        self.branches = branches


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
                repo.branches)

    return result


def host_repos_run(command, filter_repos):
    for repo_alias, repo in get_host_repos(filter_repos).items():
        print(repo_alias)
        command(repo)
        print()
        print()


def host_repos_run_with_path(command, filter_repos):
    host_repos_run(lambda repo: command(repo.path), filter_repos)


def host_repos_status(filter_repos):
    host_repos_run_with_path(ed_git_tools.status, filter_repos)

def host_repos_fetch(filter_repos):
    host_repos_run_with_path(ed_git_tools.fetch, filter_repos)

def host_repos_all_refs(filter_repos):
    host_repos_run_with_path(ed_git_tools.all_refs, filter_repos)

def handle_storage_if_available(alias, repo, handler):
    storage_path = repo.remotes.storage.get(alias)
    if storage_path is None:
        print('No repo at ' + alias + '\n')
        return
    handler(storage_path)

def fetch_storage_if_available(alias, repo):
    handle_storage_if_available(alias, repo,
        lambda path: ed_git_tools.fetch_remote(repo.path, path))

def host_repos_fetch_storage(alias, filter_repos):
    host_repos_run(lambda repo: fetch_storage_if_available(alias, repo), filter_repos)

def pull_storage_if_available(alias, repo):
    handle_storage_if_available(alias, repo,
        lambda path: ed_git_tools.pull_with_checkout_multi(repo.path, path, repo.branches))

def host_repos_pull_storage(alias, filter_repos):
    host_repos_run(lambda repo: pull_storage_if_available(alias, repo), filter_repos)

def push_storage_if_available(alias, repo):
    handle_storage_if_available(alias, repo,
        lambda path: ed_git_tools.push_all(repo.path, path))

def host_repos_push_storage(alias, filter_repos):
    host_repos_run(lambda repo: push_storage_if_available(alias, repo), filter_repos)

def pick_storage_and_handle(handler, filter_repos):
    storage = ed_storage_finder.pick_storage()
    if storage is not None:
        handler(storage, filter_repos)

def pull_repo_native(repo):
    for remote in repo.remotes.native:
        ed_git_tools.fetch_merge_with_checkout_multi(repo.path, remote, repo.branches)

def host_repos_pull_native(filter_repos):
    host_repos_run(pull_repo_native, filter_repos)

def push_repo_native(repo):
    for remote in repo.remotes.native:
        ed_git_tools.push_multi(repo.path, remote, repo.branches)

def host_repos_push_native(filter_repos):
    host_repos_run(push_repo_native, filter_repos)


def main():
    bootstrap_mode = False
    bootstrap_mode_filter = lambda: ed_git_repo_userdata.bootstrap_repos() if bootstrap_mode else None

    while True:
        action = ed_user_interaction.pick_option('Pick action', [
            'Status all',
            'Ref status all',
            'Fetch all',
            'Fetch storage all',
            'Pull storage all',
            'Push storage all',
            'Pull native all',
            'Push native all',
            'Flip bootstrap_mode',
        ])

        if action == 0:
            host_repos_status(bootstrap_mode_filter())
        elif action == 1:
            host_repos_all_refs(bootstrap_mode_filter())
        elif action == 2:
            host_repos_fetch(bootstrap_mode_filter())
        elif action == 3:
            pick_storage_and_handle(host_repos_fetch_storage, bootstrap_mode_filter())
        elif action == 4:
            pick_storage_and_handle(host_repos_pull_storage, bootstrap_mode_filter())
        elif action == 5:
            pick_storage_and_handle(host_repos_push_storage, bootstrap_mode_filter())
        elif action == 6:
            host_repos_pull_native(bootstrap_mode_filter())
        elif action == 7:
            filter_ = ed_git_repo_userdata.autopush_repos()
            if bootstrap_mode:
                filter_ &= bootstrap_mode_filter()
            host_repos_push_native(filter_)
        elif action == 8:
            bootstrap_mode = not bootstrap_mode
            print('bootstrap_mode == ' + str(bootstrap_mode))
        else:
            raise Exception('unexpected action')

        if action != 8:
            break


if __name__ == '__main__':
    ed_pause_at_end.run(main, 'Program finished successfully')
