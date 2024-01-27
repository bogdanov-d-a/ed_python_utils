import tkinter
from edpu import tkinter_utils
import pyperclip


def main() -> None:
    root = tkinter.Tk()
    root.title('Clipboard stack')

    stack: list[str] = []

    def update_out_text() -> None:
        out_text.delete(1.0, tkinter.END)
        out_text.insert(tkinter.END, '\n----------\n'.join(stack))

    def push() -> None:
        stack.append(pyperclip.paste())
        update_out_text()

    def pop() -> None:
        if len(stack) > 0:
            pyperclip.copy(stack.pop())
            update_out_text()

    push_button = tkinter.Button(root, text='Push (F6)', command=push)
    push_button.pack(side=tkinter.TOP, fill=tkinter.X)
    root.bind('<F6>', lambda _: push())

    pop_button = tkinter.Button(root, text='Pop (F7)', command=pop)
    pop_button.pack(side=tkinter.TOP, fill=tkinter.X)
    root.bind('<F7>', lambda _: pop())

    out_text = tkinter.Text(root, height=40, width=120)
    out_text_sb = tkinter.Scrollbar(root)

    out_text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    out_text_sb.pack(side=tkinter.LEFT, fill=tkinter.Y)

    out_text.config(yscrollcommand=out_text_sb.set)
    out_text_sb.config(command=out_text.yview)

    tkinter_utils.center_window(root)
    tkinter.mainloop()


if __name__ == '__main__':
    main()
