from subprocess import Popen


def popen_communicate(popen: Popen) -> None:
    with popen as process:
        process.communicate()


def popen_communicate_args(args) -> None:
    popen_communicate(Popen(args))


def popen_communicate_args_cwd(args, cwd: str) -> None:
    popen_communicate(Popen(args, cwd=cwd))
