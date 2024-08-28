from subprocess import Popen


def popen_communicate(popen: Popen) -> None:
    with popen as process:
        process.communicate()


def popen_communicate_command(command: str) -> None:
    popen_communicate(Popen(command))


def popen_communicate_command_cwd(command: str, cwd: str) -> None:
    popen_communicate(Popen(command, cwd=cwd))
