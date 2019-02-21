from tkinter import *
import ed_tkinter_utils
import ed_button_window


class CbPack:
    def __init__(self, master, text, row, command=None):
        self.var = IntVar(master)

        def command_handler():
            command(self)

        c = Checkbutton(
            master, text=text,
            variable=self.var,
            command=command_handler)
        c.grid(row=row, sticky=W)


def show_checklist(items, title):
    master = Tk()
    master.title(title)

    info_text = StringVar(master)
    info = Label(master, textvariable=info_text)
    info.grid(row=0)

    total_count = len(items)
    checked_count = 0

    def update_info_text():
        info_text.set('{0} stats: {1} / {2} ({3})'.format(
            title, checked_count, total_count - checked_count, total_count))

    update_info_text()

    def cb_command_handler(cb_pack):
        nonlocal checked_count
        if cb_pack.var.get() == 0:
            checked_count -= 1
        else:
            checked_count += 1
        update_info_text()

    row = 1
    for item in items:
        CbPack(master, item, row, cb_command_handler)
        row += 1

    ed_tkinter_utils.center_window(master)
    mainloop()


def show_picker(checklists):
    buttons = []

    def get_command(index):
        return lambda: show_checklist(checklists[index][1], checklists[index][0])

    index = 0
    for text, _ in checklists:
        buttons.append((text, get_command(index)))
        index += 1

    ed_button_window.run(buttons)
