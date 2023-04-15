from edpu import button_window
import pyperclip

def run(items):
    def get_command(index):
        def impl():
            pyperclip.copy(items[index])
            return True
        return impl

    buttons = []

    index = 0
    for item in items:
        buttons.append(('[' + item + ']', get_command(index)))
        index += 1

    button_window.run(buttons)
