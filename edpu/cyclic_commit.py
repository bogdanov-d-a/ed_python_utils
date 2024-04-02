def cyclic_commit(path: str) -> None:
    from . import pause_at_end

    def main() -> None:
        stop = False

        while not stop:
            from .citool_launcher import open_citool
            from .explorer_launcher import open_dir_in_explorer
            from .git_repo_manager.utils.git import run_command, run_git_command, status
            from .user_interaction import pick_str_option_ex

            def quit() -> None:
                nonlocal stop
                stop = True

            pick_str_option_ex(f'cyclic_commit {path}', [
                ('q', 'quit', quit),
                ('e', 'explorer', lambda: open_dir_in_explorer(path)),
                ('t', 'citool', lambda: open_citool(path)),
                ('s', 'status', lambda: status(path)),
                ('a', 'add', lambda: run_git_command(path, ['add', '.'])),
                ('c', 'commit', lambda: run_git_command(path, ['commit', '-m', '1'])),
                ('l', 'gitk', lambda: run_command(path, ['gitk'])),
                ('n', 'clean', lambda: run_git_command(path, ['clean', '-idx'])),
            ])()

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
