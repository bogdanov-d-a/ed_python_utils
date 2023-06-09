import os
import subprocess

mock = False

def run_command(path, command):
    if mock:
        print('run_command ' + path + ' ' + str(command))
        return

    with subprocess.Popen(command, cwd=path) as process:
        process.communicate()

def run_command_for_result(path, command):
    result = b''
    with subprocess.Popen(command, cwd=path, stdout=subprocess.PIPE) as process:
        for line in process.stdout.readlines():
            result += line
    return result

def put_blank_line():
    if mock:
        print('put_blank_line')
        return

    print()

def run_git_command(path, args):
    if not os.path.isdir(path):
        raise Exception(path + ' doesn\'t exist')
    run_command(path, ['git', '--no-pager'] + args)

def run_git_command_for_result(path, args):
    if not os.path.isdir(path):
        raise Exception(path + ' doesn\'t exist')
    return run_command_for_result(path, ['git', '--no-pager'] + args).decode('utf-8').rstrip('\n')

def status(path):
    run_git_command(path, ['status'])

def fetch(path):
    run_git_command(path, ['fetch', '--all'])

def fsck(path):
    run_git_command(path, ['fsck'])

def gc(path):
    run_git_command(path, ['gc'])

def all_refs(path):
    run_git_command(path, ['branch', '-av'])
    put_blank_line()
    run_git_command(path, ['tag', '--format=%(refname:strip=2) %(objectname:short)'])

def all_stash(path):
    run_git_command(path, ['stash', 'list'])

def fetch_remote(path, remote_path):
    run_git_command(path, ['fetch', remote_path])

def pull_remote(path, remote_path):
    run_git_command(path, ['pull', remote_path])

def checkout(path, branch):
    run_git_command(path, ['checkout', branch])

def create_bundle(path, file_name, refs):
    run_git_command(path, ['bundle', 'create', file_name, refs])

def rev_parse(path, ref):
    return run_git_command_for_result(path, ['rev-parse', ref])

def pull_with_checkout(path, remote_path, local_branch, remote_branch=None):
    if remote_branch is None:
        remote_branch = local_branch

    checkout(path, local_branch)
    put_blank_line()
    run_git_command(path, ['pull', remote_path, remote_branch])

def pull_with_checkout_multi(path, remote_path, branches):
    for branch in branches:
        pull_with_checkout(path, remote_path, branch)
    checkout(path, branches[0])

def push(path, remote_path, branch):
    run_git_command(path, ['push', remote_path, branch])

def push_multi(path, remote_path, branches):
    for branch in branches:
        push(path, remote_path, branch)

def push_all(path, remote_path):
    run_git_command(path, ['push', '--all', remote_path])

def init_bare(path):
    run_git_command(path, ['init', '--bare'])

def merge_with_checkout(path, remote_path, local_branch, remote_branch=None):
    if remote_branch is None:
        remote_branch = local_branch

    checkout(path, local_branch)
    put_blank_line()
    run_git_command(path, ['merge', remote_path + '/' + remote_branch])

def fetch_merge_with_checkout_multi(path, remote_path, branches):
    fetch_remote(path, remote_path)
    for branch in branches:
        merge_with_checkout(path, remote_path, branch)
    checkout(path, branches[0])
