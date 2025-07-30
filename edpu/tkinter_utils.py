from __future__ import annotations
from tkinter import Tk, Text
from typing import Callable, Optional


class Size:
    def __init__(self: Size, width: int, height: int) -> None:
        self.width = width
        self.height = height


    def scale(self: Size, multiplier: float) -> Size:
        return Size(
            int(self.width * multiplier),
            int(self.height * multiplier)
        )


    @staticmethod
    def center_calc(outer: Size, inner: Size) -> Size:
        return Size(
            center_calc(outer.width, inner.width),
            center_calc(outer.height, inner.height)
        )


def center_calc(outer: int, inner: int) -> int:
    return max(outer - inner, 0) // 2


def get_screen_size(window: Tk) -> Size:
    return Size(
        window.winfo_screenwidth(),
        window.winfo_screenheight()
    )


def non_resizable(window: Tk) -> None:
    window.resizable(False, False)


def center_window(window: Tk, size: Optional[Size]=None) -> None:
    window.update_idletasks()

    if size is None:
        size = Size(window.winfo_width(), window.winfo_height())

    screen_size = get_screen_size(window)
    offset = Size.center_calc(screen_size, size)

    window.geometry(f'{size.width}x{size.height}+{offset.width}+{offset.height}')


def autosize_window(window: Tk, multiplier: float=2/3) -> None:
    if multiplier <= 0:
        raise Exception('multiplier <= 0')

    if multiplier > 1:
        raise Exception('multiplier > 1')

    center_window(window, get_screen_size(window).scale(multiplier))


TEXT_WIDGET_START = '1.0'
TEXT_WIDGET_END = 'end'


def text_widget_get(widget: Text) -> str:
    return widget.get(TEXT_WIDGET_START, TEXT_WIDGET_END + '-1c')


def text_widget_clear(widget: Text) -> None:
    widget.delete(TEXT_WIDGET_START, TEXT_WIDGET_END)


def text_widget_set(widget: Text, text: str) -> None:
    text_widget_clear(widget)
    widget.insert(TEXT_WIDGET_END, text)


def showinfo(message: str, title: str='showinfo') -> None:
    from tkinter.messagebox import showinfo as impl
    impl(title, message)


def showerror(message: str, title: str='showerror') -> None:
    from tkinter.messagebox import showerror as impl
    impl(title, message)


def askstring(prompt: str, title: str='askstring') -> Optional[str]:
    from tkinter.simpledialog import askstring as impl
    return impl(title, prompt)


def handle_errors(fn: Callable[[], None]) -> None:
    try:
        fn()

    except:
        from traceback import format_exc
        showerror(format_exc(), 'handle_errors')
