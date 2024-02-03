import tkinter
import traceback
from typing import Callable
from . import tkinter_utils


def make_exception_wrapper(callback: Callable[[], str]) -> Callable[[], str]:
    def wrapper():
        try:
            return callback()
        except:
            return traceback.format_exc()
    return wrapper


def run(data_provider: Callable[[], str], title: str='Default title') -> None:
    root = tkinter.Tk()
    root.title(title)

    def calc() -> None:
        out_text.delete(1.0, tkinter.END)
        out_text.insert(tkinter.END, data_provider())

    root.bind('<F5>', lambda _: calc())

    calc_button = tkinter.Button(root, text='Refresh (F5)', command=calc)
    out_text = tkinter.Text(root, height=40, width=120)
    out_text_sb = tkinter.Scrollbar(root)

    calc_button.pack(side=tkinter.TOP, fill=tkinter.X)
    out_text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    out_text_sb.pack(side=tkinter.LEFT, fill=tkinter.Y)

    out_text.config(yscrollcommand=out_text_sb.set)
    out_text_sb.config(command=out_text.yview)

    calc()
    tkinter_utils.center_window(root)
    tkinter.mainloop()


def run_with_exception_wrapper(data_provider: Callable[[], str], title: str='Default title') -> None:
    run(make_exception_wrapper(data_provider), title)
