import tkinter
from typing import Any, Callable, Optional
from . import tkinter_utils


ButtonDefCb = Callable[[], Any]
ButtonDef = tuple[str, ButtonDefCb]
ButtonDefs = list[ButtonDef]


def _auto_pick(buttons: ButtonDefs, auto_pick: str) -> None:
    for text, command in buttons:
        if text == auto_pick:
            command()
            return


def _show_window(buttons: ButtonDefs) -> None:
    master: tkinter.Tk = tkinter.Tk()

    def get_command(index: int) -> Callable[[], None]:
        def impl() -> None:
            if buttons[index][1]() != False:
                master.destroy()

        return impl

    index: int = 0

    for text, _ in buttons:
        button: tkinter.Button = tkinter.Button(master, text=text, command=get_command(index))
        button.pack(side=tkinter.TOP, fill=tkinter.X)

        index += 1

    tkinter_utils.center_window(master)
    tkinter.mainloop()


def run(buttons: ButtonDefs, auto_pick: Optional[str]=None) -> None:
    if auto_pick is not None:
        _auto_pick(buttons, auto_pick)
    else:
        _show_window(buttons)
