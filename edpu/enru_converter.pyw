import tkinter
from edpu import tkinter_utils


def main() -> None:
    root = tkinter.Tk()
    root.title('EnRu converter')

    def proc_char(c: str, reverse: bool) -> str:
        data_: list[tuple[str, str]] = [
            ('`', 'ё'),
            ('~', 'Ё'),
            ('@', '"'),
            ('#', '№'),
            ('$', ';'),
            ('^', ':'),
            ('&', '?'),

            ('q', 'й'),
            ('w', 'ц'),
            ('e', 'у'),
            ('r', 'к'),
            ('t', 'е'),
            ('y', 'н'),
            ('u', 'г'),
            ('i', 'ш'),
            ('o', 'щ'),
            ('p', 'з'),
            ('[', 'х'),
            (']', 'ъ'),
            ('Q', 'Й'),
            ('W', 'Ц'),
            ('E', 'У'),
            ('R', 'К'),
            ('T', 'Е'),
            ('Y', 'Н'),
            ('U', 'Г'),
            ('I', 'Ш'),
            ('O', 'Щ'),
            ('P', 'З'),
            ('{', 'Х'),
            ('}', 'Ъ'),
            ('|', '/'),

            ('a', 'ф'),
            ('s', 'ы'),
            ('d', 'в'),
            ('f', 'а'),
            ('g', 'п'),
            ('h', 'р'),
            ('j', 'о'),
            ('k', 'л'),
            ('l', 'д'),
            (';', 'ж'),
            ('\'', 'э'),
            ('A', 'Ф'),
            ('S', 'Ы'),
            ('D', 'В'),
            ('F', 'А'),
            ('G', 'П'),
            ('H', 'Р'),
            ('J', 'О'),
            ('K', 'Л'),
            ('L', 'Д'),
            (':', 'Ж'),
            ('"', 'Э'),

            ('z', 'я'),
            ('x', 'ч'),
            ('c', 'с'),
            ('v', 'м'),
            ('b', 'и'),
            ('n', 'т'),
            ('m', 'ь'),
            (',', 'б'),
            ('.', 'ю'),
            ('/', '.'),
            ('Z', 'Я'),
            ('X', 'Ч'),
            ('C', 'С'),
            ('V', 'М'),
            ('B', 'И'),
            ('N', 'Т'),
            ('M', 'Ь'),
            ('<', 'Б'),
            ('>', 'Ю'),
            ('?', ','),
        ]

        for d in data_:
            if not reverse:
                if c == d[0]:
                    return d[1]
            else:
                if c == d[1]:
                    return d[0]

        return c

    def proc_text(text: str, reverse: bool) -> str:
        result = ''
        for c in text:
            result += proc_char(c, reverse)
        return result

    def convert(reverse: bool) -> None:
        text_data = text.get("1.0", tkinter.END)
        text_data = proc_text(text_data, reverse)
        text.delete(1.0, tkinter.END)
        text.insert(tkinter.END, text_data)

    button = tkinter.Button(root, text='En->Ru (F5)', command=lambda: convert(False))
    button.pack(side=tkinter.TOP, fill=tkinter.X)
    root.bind('<F5>', lambda _: convert(False))

    buttonRev = tkinter.Button(root, text='Ru->En (F6)', command=lambda: convert(True))
    buttonRev.pack(side=tkinter.TOP, fill=tkinter.X)
    root.bind('<F6>', lambda _: convert(True))

    text = tkinter.Text(root, height=40, width=120)
    text_sb = tkinter.Scrollbar(root)

    text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    text_sb.pack(side=tkinter.LEFT, fill=tkinter.Y)

    text.config(yscrollcommand=text_sb.set)
    text_sb.config(command=text.yview)

    tkinter_utils.center_window(root)
    tkinter.mainloop()


if __name__ == '__main__':
    main()
