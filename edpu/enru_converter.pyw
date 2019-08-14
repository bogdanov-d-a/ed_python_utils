from tkinter import *
import edpu.tkinter_utils


def main():
    root = Tk()
    root.title('EnRu converter')

    def proc_char(c, reverse):
        data_ = [
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

    def proc_text(text, reverse):
        result = ''
        for c in text:
            result += proc_char(c, reverse)
        return result

    def convert(reverse):
        text_data = text.get("1.0", END)
        text_data = proc_text(text_data, reverse)
        text.delete(1.0, END)
        text.insert(END, text_data)

    button = Button(root, text='En->Ru (F5)', command=lambda: convert(False))
    button.pack(side=TOP, fill=X)
    root.bind('<F5>', lambda e: convert(False))

    buttonRev = Button(root, text='Ru->En (F6)', command=lambda: convert(True))
    buttonRev.pack(side=TOP, fill=X)
    root.bind('<F6>', lambda e: convert(True))

    text = Text(root, height=40, width=120)
    text_sb = Scrollbar(root)

    text.pack(side=LEFT, fill=Y)
    text_sb.pack(side=LEFT, fill=Y)

    text.config(yscrollcommand=text_sb.set)
    text_sb.config(command=text.yview)

    edpu.tkinter_utils.center_window(root)
    mainloop()


if __name__ == '__main__':
    main()
