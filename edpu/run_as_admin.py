from typing import Optional


def run_as_admin(file: str, parameters: Optional[str]=None, directory: Optional[str]=None) -> None:
    import ctypes
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', file, parameters, directory, 1)
