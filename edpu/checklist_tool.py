from __future__ import annotations
import tkinter
from typing import Callable
from . import tkinter_utils
from . import button_window


Command = Callable[[], bool]


class CbPack:
    def __init__(self: CbPack, master: tkinter.Tk, text: str, row: int, command: Callable[[CbPack], None]) -> None:
        self.var = tkinter.IntVar(master)

        checkbutton = tkinter.Checkbutton(
            master,
            text=text,
            variable=self.var,
            command=lambda: command(self)
        )

        checkbutton.grid(row=row, sticky=tkinter.W)


def show_checklist(items: list[str], title: str) -> None:
    master = tkinter.Tk()
    master.title(title)

    info_text = tkinter.StringVar(master)
    info = tkinter.Label(master, textvariable=info_text)
    info.grid(row=0)

    total_count: int = len(items)
    checked_count: int = 0

    def update_info_text() -> None:
        info_text.set('{0} stats: {1} / {2} ({3})'.format(
            title, checked_count, total_count - checked_count, total_count))

    update_info_text()

    def cb_command_handler(cb_pack: CbPack) -> None:
        nonlocal checked_count
        if cb_pack.var.get() == 0:
            checked_count -= 1
        else:
            checked_count += 1
        update_info_text()

    row: int = 1
    for item in items:
        CbPack(master, item, row, cb_command_handler)
        row += 1

    tkinter_utils.center_window(master)
    tkinter.mainloop()


def show_picker(checklists: list[tuple[str, list[str]]]) -> None:
    buttons: list[tuple[str, Command]] = []

    def get_command(index: int) -> Command:
        def command() -> bool:
            show_checklist(checklists[index][1], checklists[index][0])
            return False

        return command

    index: int = 0
    for text, _ in checklists:
        buttons.append((text, get_command(index)))
        index += 1

    button_window.run(buttons)
