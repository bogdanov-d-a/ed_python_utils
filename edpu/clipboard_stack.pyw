from tkinter import *
import edpu.tkinter_utils
import pyperclip


def main():
    root = Tk()
    root.title('Clipboard stack')

    stack = []

    def update_out_text():
        out_text.delete(1.0, END)
        out_text.insert(END, '\n----------\n'.join(stack))

    def push():
        stack.append(pyperclip.paste())
        update_out_text()

    def pop():
        if len(stack) > 0:
            pyperclip.copy(stack.pop())
            update_out_text()

    push_button = Button(root, text='Push (F6)', command=push)
    push_button.pack(side=TOP, fill=X)
    root.bind('<F6>', lambda e: push())

    pop_button = Button(root, text='Pop (F7)', command=pop)
    pop_button.pack(side=TOP, fill=X)
    root.bind('<F7>', lambda e: pop())

    out_text = Text(root, height=40, width=120)
    out_text_sb = Scrollbar(root)

    out_text.pack(side=LEFT, fill=Y)
    out_text_sb.pack(side=LEFT, fill=Y)

    out_text.config(yscrollcommand=out_text_sb.set)
    out_text_sb.config(command=out_text.yview)

    edpu.tkinter_utils.center_window(root)
    mainloop()


if __name__ == '__main__':
    main()
