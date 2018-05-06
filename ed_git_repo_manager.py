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


def get_host_repos():
    host = ed_host_alias.get()
    result = {}

    for repo_alias, repo in ed_git_repo_userdata.get().items():
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


def host_repos_run_and_print(command):
    for repo_alias, repo in get_host_repos().items():
        print(repo_alias)
        print(command(repo))
        print()


def host_repos_run_with_path_and_print(command):
    host_repos_run_and_print(lambda repo: command(repo.path))


def host_repos_status():
    host_repos_run_with_path_and_print(ed_git_tools.status)

def host_repos_fetch():
    host_repos_run_with_path_and_print(ed_git_tools.fetch)

def host_repos_all_refs():
    host_repos_run_with_path_and_print(ed_git_tools.all_refs)

def handle_storage_if_available(alias, repo, handler):
    storage_path = repo.remotes.storage.get(alias)
    if storage_path is None:
        return 'No repo at ' + alias + '\n'
    return handler(storage_path)

def fetch_storage_if_available(alias, repo):
    return handle_storage_if_available(alias, repo,
        lambda path: ed_git_tools.fetch_storage(repo.path, path))

def host_repos_fetch_storage(alias):
    host_repos_run_and_print(lambda repo: fetch_storage_if_available(alias, repo))

def pull_storage_if_available(alias, repo):
    return handle_storage_if_available(alias, repo,
        lambda path: ed_git_tools.pull_storage_multi(repo.path, path, repo.branches))

def host_repos_pull_storage(alias):
    host_repos_run_and_print(lambda repo: pull_storage_if_available(alias, repo))

def pick_storage_and_handle(handler):
        storage = ed_storage_finder.pick_storage()
        if storage is not None:
            handler(storage)


def main():
    action = ed_user_interaction.pick_option('Pick action', [
        'Status all',
        'Fetch all',
        'Ref status all',
        'Fetch storage all',
        'Pull storage all',
    ])

    if action == 0:
        host_repos_status()
    elif action == 1:
        host_repos_fetch()
    elif action == 2:
        host_repos_all_refs()
    elif action == 3:
        pick_storage_and_handle(host_repos_fetch_storage)
    elif action == 4:
        pick_storage_and_handle(host_repos_pull_storage)
    else:
        raise Exception('unexpected action')


if __name__ == '__main__':
    ed_pause_at_end.run(main, 'Program finished successfully')
