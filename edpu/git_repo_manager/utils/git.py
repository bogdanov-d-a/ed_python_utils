from typing import Optional


mock = False


def run_command(path: str, command: list[str]) -> None:
    if mock:
        print('run_command ' + path + ' ' + str(command))
        return

    from subprocess import Popen

    with Popen(command, cwd=path) as process:
        process.communicate()


def run_command_for_result(path: str, command: list[str]) -> bytes:
    from subprocess import Popen, PIPE

    result = b''

    with Popen(command, cwd=path, stdout=PIPE) as process:
        if process.stdout is None:
            raise Exception()

        for line in process.stdout.readlines():
            result += line

    return result


def put_blank_line() -> None:
    if mock:
        print('put_blank_line')
        return

    print()


def run_git_command(path: str, args: list[str]) -> None:
    from os.path import isdir

    if not isdir(path):
        raise Exception(path + ' doesn\'t exist')

    run_command(path, ['git', '--no-pager'] + args)


def run_git_command_for_result(path: str, args: list[str]) -> str:
    from os.path import isdir

    if not isdir(path):
        raise Exception(path + ' doesn\'t exist')

    return run_command_for_result(path, ['git', '--no-pager'] + args).decode('utf-8').rstrip('\n')


def status(path: str) -> None:
    run_git_command(path, ['status'])


def remotes(path: str) -> None:
    run_git_command(path, ['remote', '-vv'])


def fetch(path: str) -> None:
    run_git_command(path, ['fetch', '--all'])


def fsck(path: str) -> None:
    run_git_command(path, ['fsck'])


def gc(path: str) -> None:
    run_git_command(path, ['gc'])


def all_refs(path: str) -> None:
    run_git_command(path, ['branch', '-av'])
    put_blank_line()
    run_git_command(path, ['tag', '--format=%(refname:strip=2) %(objectname:short)'])


def all_stash(path: str) -> None:
    run_git_command(path, ['stash', 'list'])


def fetch_remote(path: str, remote_path: str) -> None:
    run_git_command(path, ['fetch', remote_path])


def pull_remote(path: str, remote_path: str) -> None:
    run_git_command(path, ['pull', remote_path])


def checkout(path: str, branch: str, orphan: bool=False) -> None:
    run_git_command(path, ['checkout'] + (['--orphan'] if orphan else []) + [branch])


def create_bundle(path: str, file_name: str, refs: str) -> None:
    run_git_command(path, ['bundle', 'create', file_name, refs])


def rename(path: str, name: str) -> None:
    run_git_command(path, ['branch', '-M', name])


def reset_hard(path: str) -> None:
    run_git_command(path, ['reset', '--hard'])


def clean_ffdx(path: str) -> None:
    run_git_command(path, ['clean', '-ffdx'])


def worktree_add_detach(path: str, worktree_path: str, revision: str) -> None:
    run_git_command(path, ['worktree', 'add', '--detach', worktree_path, revision])


def rev_parse(path: str, ref: str) -> str:
    return run_git_command_for_result(path, ['rev-parse', ref])


def pull_with_checkout(path: str, remote_path: str, local_branch: str, remote_branch: Optional[str]=None, orphan: bool=False) -> None:
    if remote_branch is None:
        remote_branch = local_branch

    checkout(path, local_branch, orphan)

    if orphan:
        reset_hard(path)

    put_blank_line()
    run_git_command(path, ['pull', remote_path, remote_branch])


def pull_with_checkout_multi(path: str, remote_path: str, branches: list[str], orphan: bool=False) -> None:
    for branch in branches:
        pull_with_checkout(path, remote_path, branch, orphan=(orphan and branch != branches[0]))

    checkout(path, branches[0])


def push(path: str, remote_path: str, branch: str) -> None:
    run_git_command(path, ['push', remote_path, branch])


def push_multi(path: str, remote_path: str, branches: list[str]) -> None:
    for branch in branches:
        push(path, remote_path, branch)


def push_all(path: str, remote_path: str) -> None:
    run_git_command(path, ['push', '--all', remote_path])


def init(path: str) -> None:
    run_git_command(path, ['init'])


def init_bare(path: str) -> None:
    run_git_command(path, ['init', '--bare'])


def merge_with_checkout(path: str, remote_path: str, local_branch: str, remote_branch: Optional[str]=None) -> None:
    if remote_branch is None:
        remote_branch = local_branch

    checkout(path, local_branch)
    put_blank_line()
    run_git_command(path, ['merge', remote_path + '/' + remote_branch])


def fetch_merge_with_checkout_multi(path: str, remote_path: str, branches: list[str]) -> None:
    fetch_remote(path, remote_path)

    for branch in branches:
        merge_with_checkout(path, remote_path, branch)

    checkout(path, branches[0])
