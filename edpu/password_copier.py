def run(data: dict[str, str]) -> None:
    aliases = sorted(data.keys())

    while True:
        from .user_interaction import pick_option
        from pyperclip import copy

        index = pick_option('Pick alias', aliases)
        alias = aliases[index]
        copy(data[alias])
        print('Copied ' + alias)
        print()
