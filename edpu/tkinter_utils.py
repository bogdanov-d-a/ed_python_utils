from tkinter import Tk
from typing import Callable


def center_window(win: Tk) -> None:
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def showinfo(message: str, title: str='showinfo') -> None:
    from tkinter import messagebox
    messagebox.showinfo(title, message)


def handle_errors(fn: Callable[[], None]) -> None:
    try:
        fn()

    except:
        from tkinter import messagebox
        from traceback import format_exc

        messagebox.showerror('handle_errors', format_exc())
