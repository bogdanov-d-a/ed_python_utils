def _start_d(cwd: str, cmd: str) -> None:
    from .start_d import start_d
    from os import system
    system(start_d(cwd, cmd))


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
        ('l', 'clipboard', _clipboard),
        ('c', 'cmd', lambda path: _start_d(path, f'cmd')),
        ('e', 'explorer', open_dir_in_explorer),
    ])(path)
