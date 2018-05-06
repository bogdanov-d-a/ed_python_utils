import ed_git_repo_userdata
import ed_host_alias
import ed_path_manager
import ed_git_tools
import ed_user_interaction
import ed_pause_at_end


class Data:
    def __init__(self, path, remotes):
        self.path = path
        self.remotes = remotes


def get_host_repos():
    host = ed_host_alias.get()
    result = {}
    for repo_alias, repo in ed_git_repo_userdata.get().items():
        path_alias = repo.host_to_path.get(host)
        if path_alias is not None:
            path = ed_path_manager.get_host_data().get(path_alias)
            result[repo_alias] = Data(path, repo.remotes)
    return result


def host_repos_run_and_print(command):
    for repo_alias, repo in get_host_repos().items():
        print(repo_alias)
        print(command(repo.path))
        print()


def host_repos_status():
    host_repos_run_and_print(ed_git_tools.status)

def host_repos_fetch():
    host_repos_run_and_print(ed_git_tools.fetch)


def main():
    action = ed_user_interaction.pick_option('Pick action', [
        'Status all',
        'Fetch all',
    ])

    if (action == 0):
        host_repos_status()
    elif (action == 1):
        host_repos_fetch()
    else:
        raise Exception('unexpected action')


if __name__ == '__main__':
    ed_pause_at_end.run(main, 'Program finished successfully')
