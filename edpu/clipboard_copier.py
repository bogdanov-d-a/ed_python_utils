from typing import Callable
from edpu import button_window
import pyperclip


def run(items: list[str]) -> None:
    def get_command(index: int) -> Callable[[], bool]:
        def impl() -> bool:
            pyperclip.copy(items[index])
            return True

        return impl

    buttons: button_window.ButtonDefs = []

    index: int = 0
    for item in items:
        buttons.append(('[' + item + ']', get_command(index)))
        index += 1

    button_window.run(buttons)
