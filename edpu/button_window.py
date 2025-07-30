from typing import Any, Callable, Optional


ButtonCommand = Callable[[], Any]
ButtonDef = tuple[str, ButtonCommand]
ButtonDefs = list[ButtonDef]


def run(button_defs: ButtonDefs, title: Optional[str]=None) -> None:
    from .tkinter_utils import non_resizable, center_window
    from tkinter import Tk


    root = Tk()
    root.title(title)
    non_resizable(root)


    for name, command in button_defs:
        from tkinter import TOP, X
        from tkinter.ttk import Button

        def get_command() -> ButtonCommand:
            command_copy = command

            def impl() -> None:
                if command_copy() != False:
                    root.destroy()

            return impl

        Button(
            root,
            text=name,
            command=get_command()
        ).pack(side=TOP, fill=X)


    center_window(root)
    root.mainloop()
