def show(text: str) -> None:
    from edpu.tkinter_utils import non_resizable
    from tkinter import Tk
    from tkinter.ttk import Label

    root = Tk()
    root.title('show_text')
    non_resizable(root)

    Label(
        root,
        font=('Sans Serif', 128),
        text=text
    ).pack(expand=True)

    root.mainloop()


def main() -> None:
    from edpu.tkinter_utils import askstring, showerror
    text = askstring('Enter text to show:')

    if text is None:
        showerror('No text provided')
    else:
        show(text)


if __name__ == '__main__':
    main()
