from __future__ import annotations
from typing import Callable
import tkinter


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
    from . import tkinter_utils

    master = tkinter.Tk()
    master.title(title)

    info_text = tkinter.StringVar(master)
    info = tkinter.Label(master, textvariable=info_text)
    info.grid(row=0)

    total_count = len(items)
    checked_count = 0

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

    for item, row in zip(items, range(len(items))):
        CbPack(master, item, row + 1, cb_command_handler)

    tkinter_utils.center_window(master)
    tkinter.mainloop()


def show_picker(checklists: list[tuple[str, list[str]]]) -> None:
    from . import button_window

    buttons: list[tuple[str, Command]] = []

    def get_command(index: int) -> Command:
        def command() -> bool:
            show_checklist(checklists[index][1], checklists[index][0])
            return False

        return command

    for text, index in zip(list(map(lambda checklist: checklist[0], checklists)), range(len(checklists))):
        buttons.append((text, get_command(index)))

    button_window.run(buttons)
