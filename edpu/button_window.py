from tkinter import *
from . import tkinter_utils


def run(buttons, auto_pick=None):
    if auto_pick is not None:
        for text, command in buttons:
            if text == auto_pick:
                command()
        return

    master = Tk()

    def get_command(index):
        def impl():
            if buttons[index][1]():
                master.destroy()
        return impl

    index = 0
    for text, _ in buttons:
        b = Button(master, text=text, command=get_command(index))
        b.pack(side=TOP, fill=X)
        index += 1

    tkinter_utils.center_window(master)
    mainloop()
