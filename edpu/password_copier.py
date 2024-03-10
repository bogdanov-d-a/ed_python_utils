def run(data: dict[str, str]) -> None:
    from . import pause_at_end

    def impl() -> None:
        aliases = sorted(data.keys())

        while True:
            from .user_interaction import pick_option
            from pyperclip import copy

            index = pick_option('Pick alias', aliases)
            alias = aliases[index]
            copy(data[alias])
            print('Copied ' + alias)
            print()

    pause_at_end.run(impl, pause_at_end.DEFAULT_MESSAGE)
