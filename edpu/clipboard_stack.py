from typing import Callable


VoidFn = Callable[[], None]


def main() -> None:
    from .tkinter_utils import autosize_window
    from tkinter import Tk, NSEW
    from tkinter.scrolledtext import ScrolledText

    root = Tk()
    root.title('clipboard_stack')
    root.columnconfigure(0, weight=1)

    def init_data() -> tuple[VoidFn, VoidFn]:
        data: list[str] = []

        def update() -> None:
            from .tkinter_utils import text_widget_set
            text_widget_set(text, f'\n{'-' * 64}\n'.join(data))

        def push() -> None:
            from pyperclip import paste
            data.append(paste())
            update()

        def pop() -> None:
            if len(data) > 0:
                from pyperclip import copy
                copy(data.pop())
                update()

        return (push, pop)

    push, pop = init_data()

    def add_buttons() -> None:
        from tkinter.ttk import Frame

        root.rowconfigure(0)
        frame = Frame(root)
        frame.grid(row=0, column=0, sticky=NSEW)
        frame.rowconfigure(0, weight=1)

        def add_button(name: str, key: str, command: VoidFn, column: int) -> None:
            frame.columnconfigure(column, weight=1)

            from tkinter.ttk import Button
            Button(
                frame,
                text=f'{name} ({key})',
                command=command
            ).grid(row=0, column=column, sticky=NSEW)

            from .string_utils import angle_brackets_wrap
            root.bind(angle_brackets_wrap(key), lambda _: command())

        add_button('Push', 'F6', push, 0)
        add_button('Pop', 'F7', pop, 1)

    add_buttons()

    root.rowconfigure(1, weight=1)
    text = ScrolledText(root)
    text.grid(row=1, column=0, sticky=NSEW)

    autosize_window(root)
    root.mainloop()
