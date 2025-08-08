from typing import Callable, Optional


StrFn = Callable[[], str]


def make_exception_wrapper(fn: StrFn) -> StrFn:
    def impl() -> str:
        try:
            return fn()

        except:
            from traceback import format_exc
            return format_exc()

    return impl


def run(data_provider: StrFn, title: Optional[str]=None) -> None:
    from .tkinter_utils import autosize_window
    from tkinter import Tk, NSEW
    from tkinter.ttk import Button
    from tkinter.scrolledtext import ScrolledText

    root = Tk()
    root.title(title)
    root.columnconfigure(0, weight=1)

    def update() -> None:
        from .tkinter_utils import text_widget_set
        text_widget_set(text, data_provider())

    root.bind('<F5>', lambda _: update())

    root.rowconfigure(0)
    Button(
        root,
        text='Refresh (F5)',
        command=update
    ).grid(row=0, column=0, sticky=NSEW)

    root.rowconfigure(1, weight=1)
    text = ScrolledText(root)
    text.grid(row=1, column=0, sticky=NSEW)

    update()

    autosize_window(root)
    root.mainloop()


def run_with_exception_wrapper(data_provider: StrFn, title: Optional[str]=None) -> None:
    run(make_exception_wrapper(data_provider), title)
