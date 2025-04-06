from typing import Optional


def _start(args: list[str], path: Optional[str]=None) -> None:
    from .win_start import start
    from os import system
    system(start(args, path))


def _clipboard(path: str) -> None:
    from pyperclip import copy
    copy(path)
    print(f'Copied {path}')
    input()


def run(name: str, dirs: list[tuple[str, str, str]]) -> None:
    from .explorer_launcher import open_dir_in_explorer
    from .user_interaction import pick_str_option_ex

    path = pick_str_option_ex(f'favorite_dirs_manager {name} path', dirs)

    pick_str_option_ex(f'favorite_dirs_manager {name} action', [
        ('w', 'clipboard', _clipboard),
        ('r', 'cmd', lambda path: _start(['cmd'], path)),
        ('e', 'explorer', open_dir_in_explorer),
    ])(path)
