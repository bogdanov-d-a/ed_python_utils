def run(items: list[str]) -> None:
    from . import button_window
    from typing import Callable

    def get_command(index: int) -> Callable[[], bool]:
        def impl() -> bool:
            from pyperclip import copy
            copy(items[index])
            return True

        return impl

    buttons: button_window.ButtonDefs = []

    for item, index in zip(items, range(len(items))):
        buttons.append(('[' + item + ']', get_command(index)))

    button_window.run(buttons)
