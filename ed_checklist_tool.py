from tkinter import *
import ed_tkinter_utils


class CbPack:
    def __init__(self, master, text, row, command=None):
        self.var = IntVar()
        c = Checkbutton(
            master, text=text,
            variable=self.var,
            command=command)
        c.grid(row=row, sticky=W)


def show_checklist(items):
    master = Tk()

    row = 0
    for item in items:
        CbPack(master, item, row)
        row += 1

    ed_tkinter_utils.center_window(master)
    mainloop()


def show_picker(checklists):
    master = Tk()

    def get_command(index):
        return lambda: show_checklist(checklists[index][1])

    index = 0
    for text, _ in checklists:
        b = Button(master, text=text, command=get_command(index))
        b.pack(side=TOP, fill=X)
        index += 1

    ed_tkinter_utils.center_window(master)
    mainloop()
