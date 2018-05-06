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

def fetch_remote(path, remote_path):
    return run_command(path, ['git', 'fetch', remote_path])

def checkout(path, branch):
    return run_command(path, ['git', 'checkout', branch])

def pull_with_checkout(path, remote_path, local_branch, remote_branch=None):
    if remote_branch is None:
        remote_branch = local_branch

    result = checkout(path, local_branch)
    result += '\n' + run_command(path, ['git', 'pull', remote_path, remote_branch])
    return result

def pull_with_checkout_multi(path, remote_path, branches):
    result = ''
    for branch in branches:
        result += pull_with_checkout(path, remote_path, branch)
    result += checkout(path, branches[0])
    return result

def push_all(path, remote_path):
    return run_command(path, ['git', 'push', '--all', remote_path])

def merge_with_checkout(path, remote_path, local_branch, remote_branch=None):
    if remote_branch is None:
        remote_branch = local_branch

    result = checkout(path, local_branch)
    result += '\n' + run_command(path, ['git', 'merge', remote_path + '/' + remote_branch])
    return result

def fetch_merge_with_checkout_multi(path, remote_path, branches):
    result = fetch_remote(path, remote_path)
    for branch in branches:
        result += merge_with_checkout(path, remote_path, branch)
    result += checkout(path, branches[0])
    return result
