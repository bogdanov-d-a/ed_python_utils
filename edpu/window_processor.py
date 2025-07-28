from typing import Callable, Optional


StrProcFn = Callable[[str], str]
VoidFn = Callable[[], None]
Actions = list[tuple[str, StrProcFn]]


def make_exception_wrapper(fn: StrProcFn) -> StrProcFn:
    def impl(s: str) -> str:
        try:
            return fn(s)

        except:
            from traceback import format_exc
            return format_exc()

    return impl


def run(actions: Actions, title: Optional[str]=None) -> None:
    from .tkinter_utils import autosize_window
    from tkinter import Tk
    from tkinter.scrolledtext import ScrolledText

    root = Tk()
    root.title(title)
    root.bind('<Escape>', lambda _: root.destroy())
    root.columnconfigure(0, weight=1)

    def add_buttons() -> None:
        from tkinter import NSEW
        from tkinter.ttk import Frame

        root.rowconfigure(0)
        frame = Frame(root)
        frame.grid(row=0, column=0, sticky=NSEW)
        frame.rowconfigure(0, weight=1)

        def get_actions_raw() -> list[tuple[str, VoidFn]]:
            from .tkinter_utils import text_widget_get, text_widget_set

            def paste_left() -> None:
                from pyperclip import paste
                text_widget_set(left, paste())

            def copy_right() -> None:
                from pyperclip import copy
                copy(text_widget_get(right))

            def clear_right() -> None:
                from .tkinter_utils import text_widget_clear
                text_widget_clear(right)

            def swap() -> None:
                str_left = text_widget_get(left)
                str_right = text_widget_get(right)

                text_widget_set(left, str_right)
                text_widget_set(right, str_left)

            return list(map(
                lambda action: (
                    action[0],
                    lambda: text_widget_set(right, action[1](text_widget_get(left)))
                ),
                actions
            )) + [
                ('Paste left', paste_left),
                ('Copy right', copy_right),
                ('Clear right', clear_right),
                ('Swap', swap),
            ]

        def add_button(name: str, bind_name: str, bind_sequence: str, fn: VoidFn, column: int) -> None:
            from tkinter.ttk import Button
            frame.columnconfigure(column, weight=1)
            Button(frame, text=f'{name} ({bind_name})', command=fn).grid(row=0, column=column, sticky=NSEW)
            root.bind(bind_sequence, lambda _: fn())

        def impl() -> None:
            actions_raw = get_actions_raw()

            if len(actions_raw) == 0:
                raise Exception('len(actions_raw) == 0')

            bind_index = 12 + 1 - len(actions_raw)

            if bind_index < 1:
                raise Exception('bind_index < 1')

            column = 0

            for action_name, action_fn in actions_raw:
                from .string_utils import angle_brackets_wrap

                bind_name = f'F{bind_index}'

                add_button(
                    action_name,
                    bind_name,
                    angle_brackets_wrap(bind_name),
                    action_fn,
                    column
                )

                bind_index += 1
                column += 1

        impl()

    add_buttons()

    def add_texts() -> tuple[ScrolledText, ScrolledText]:
        from tkinter import NSEW
        from tkinter.ttk import Frame

        root.rowconfigure(1, weight=1)
        frame = Frame(root)
        frame.grid(row=1, column=0, sticky=NSEW)
        frame.rowconfigure(0, weight=1)

        def add_text(column: int) -> ScrolledText:
            frame.columnconfigure(column, weight=1)
            text = ScrolledText(frame)
            text.grid(row=0, column=column, sticky=NSEW)
            return text

        left = add_text(0)
        right = add_text(1)

        return (left, right)

    left, right = add_texts()

    autosize_window(root)
    root.mainloop()


def run_with_exception_wrappers(actions: Actions, title: Optional[str]=None) -> None:
    run(list(map(
        lambda action: (action[0], make_exception_wrapper(action[1])),
        actions
    )), title)
