if __name__ == '__main__':
    print('clipboard_beep')

    last = ''

    while True:
        from time import sleep

        try:
            from pyperclip import paste
            now = paste()
        except:
            now = ''

        if last != now:
            from winsound import Beep

            print('beep')

            Beep(2400, 100)
            sleep(0.1)
            Beep(2800, 100)

            last = now

        sleep(0.05)
