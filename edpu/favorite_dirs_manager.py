def _clipboard(path: str) -> None:
    from pyperclip import copy
    copy(path)
    print(f'Copied {path}')
    input()


def run(name: str, dirs: list[tuple[str, str, str]]) -> None:
    from .explorer_launcher import open_dir_in_explorer
    from .user_interaction import pick_str_option_ex
    from .win_start import start_run

    path = pick_str_option_ex(f'favorite_dirs_manager {name} path', dirs)

    pick_str_option_ex(f'favorite_dirs_manager {name} action', [
        ('w', 'clipboard', _clipboard),
        ('r', 'cmd', lambda path: start_run(['cmd'], path)),
        ('e', 'explorer', open_dir_in_explorer),
    ])(path)
