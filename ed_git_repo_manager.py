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
    def __init__(self, path, remotes):
        self.path = path
        self.remotes = remotes


def get_host_repos():
    host = ed_host_alias.get()
    storage = ed_storage_finder.find_all_storage()
    storage_path_data = ed_storage_path_data.get()

    result = {}

    for repo_alias, repo in ed_git_repo_userdata.get().items():
        path_alias = repo.host_to_path.get(host)
        if path_alias is not None:
            path = ed_path_manager.get_host_data().get(path_alias)

            storage_remotes = {}
            for storage_alias, storage_path_alias in repo.remotes.storage.items():
                storage_path_root = storage.get(storage_alias)
                if storage_path_root is not None:
                    storage_path = storage_path_data.get(storage_alias).get(storage_path_alias)
                    storage_remotes[storage_alias] = storage_path_root + storage_path

            result[repo_alias] = Data(path,
                ed_git_repo_data.Remotes(repo.remotes.native, storage_remotes))

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

def fetch_storage_if_available(alias, repo):
    storage_path = repo.remotes.storage.get(alias)
    if storage_path is None:
        return 'No repo at ' + alias + '\n'
    return ed_git_tools.fetch_storage(repo.path, storage_path)

def host_repos_fetch_storage(alias):
    host_repos_run_and_print(lambda repo: fetch_storage_if_available(alias, repo))


def main():
    action = ed_user_interaction.pick_option('Pick action', [
        'Status all',
        'Fetch all',
        'Ref status all',
        'Fetch storage all',
    ])

    if action == 0:
        host_repos_status()
    elif action == 1:
        host_repos_fetch()
    elif action == 2:
        host_repos_all_refs()
    elif action == 3:
        host_repos_fetch_storage(ed_storage_finder.pick_storage())
    else:
        raise Exception('unexpected action')


if __name__ == '__main__':
    ed_pause_at_end.run(main, 'Program finished successfully')
