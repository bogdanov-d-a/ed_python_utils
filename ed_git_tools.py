import subprocess

def run_command(path, command):
    with subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path) as process:
        return process.communicate()[0].decode('utf-8')

def status(path):
    return run_command(path, ['git', 'status'])

def fetch(path):
    return run_command(path, ['git', 'fetch', '--all'])

def all_refs(path):
    result = run_command(path, ['git', 'branch', '-av'])
    result += '\n' + run_command(path, ['git', 'tag', '--format=%(refname:strip=2) %(objectname:short)'])
    result += '\n' + run_command(path, ['git', 'stash', 'list'])
    return result

def fetch_storage(path, remote_path):
    return run_command(path, ['git', 'fetch', remote_path])

def checkout(path, branch):
    return run_command(path, ['git', 'checkout', branch])

def pull_storage(path, remote_path, local_branch, remote_branch=None):
    if remote_branch is None:
        remote_branch = local_branch

    result = checkout(path, local_branch)
    result += '\n' + run_command(path, ['git', 'pull', remote_path, remote_branch])
    return result

def pull_storage_multi(path, remote_path, branches):
    result = ''
    for branch in branches:
        result += pull_storage(path, remote_path, branch)
    result += checkout(path, branches[0])
    return result
