def open_citool(path: str) -> None:
    from subprocess import Popen
    Popen('git citool', cwd=path)
