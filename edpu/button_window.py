from typing import Any, Callable, Optional


ButtonDefCb = Callable[[], Any]
ButtonDef = tuple[str, ButtonDefCb]
ButtonDefs = list[ButtonDef]


def _auto_pick(button_defs: ButtonDefs, auto_pick: str) -> None:
    for text, command in button_defs:
        if text == auto_pick:
            command()
            return


def _show_window(button_defs: ButtonDefs) -> None:
    from . import tkinter_utils
    import tkinter

    master = tkinter.Tk()

    def get_command(index: int) -> Callable[[], None]:
        def impl() -> None:
            if button_defs[index][1]() != False:
                master.destroy()

        return impl

    for button_text, index in zip(list(map(lambda button_def: button_def[0], button_defs)), range(len(button_defs))):
        button = tkinter.Button(master, text=button_text, command=get_command(index))
        button.pack(side=tkinter.TOP, fill=tkinter.X)

    tkinter_utils.center_window(master)
    tkinter.mainloop()


def run(button_defs: ButtonDefs, auto_pick: Optional[str]=None) -> None:
    if auto_pick is not None:
        _auto_pick(button_defs, auto_pick)
    else:
        _show_window(button_defs)
