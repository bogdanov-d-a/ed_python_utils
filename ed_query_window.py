import tkinter


def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def run(data_provider):
    root = tkinter.Tk()

    def calc():
        out_text.delete(1.0, tkinter.END)
        out_text.insert(tkinter.END, data_provider())

    root.bind('<F5>', lambda e: calc())

    calc_button = tkinter.Button(root, command=calc)
    out_text = tkinter.Text(root, height=40, width=120)
    out_text_sb = tkinter.Scrollbar(root)

    calc_button.pack(side=tkinter.TOP, fill=tkinter.X)
    out_text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    out_text_sb.pack(side=tkinter.LEFT, fill=tkinter.Y)

    out_text.config(yscrollcommand=out_text_sb.set)
    out_text_sb.config(command=out_text.yview)

    center_window(root)

    tkinter.mainloop()
