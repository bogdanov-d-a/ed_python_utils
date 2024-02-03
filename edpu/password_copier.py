from edpu import user_interaction
import pyperclip

def run(data: dict[str, str]) -> None:
    aliases = sorted(data.keys())

    while True:
        index = user_interaction.pick_option('Pick alias', aliases)
        alias = aliases[index]
        pyperclip.copy(data[alias])
        print('Copied ' + alias)
        print()
