from tkinter import *
import ed_tkinter_utils


def run(buttons):
    master = Tk()

    def get_command(index):
        def impl():
            master.destroy()
            return buttons[index][1]()
        return impl

    index = 0
    for text, _ in buttons:
        b = Button(master, text=text, command=get_command(index))
        b.pack(side=TOP, fill=X)
        index += 1

    ed_tkinter_utils.center_window(master)
    mainloop()
