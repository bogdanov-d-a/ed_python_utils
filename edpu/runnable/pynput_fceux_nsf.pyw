if __name__ == '__main__':
    from edpu.button_window import run
    from edpu.pynput_ex import ControllerEx
    from pynput.keyboard import Key
    from typing import Any, Callable

    c = ControllerEx()

    def get_false_returner(fn: Callable[[], Any]) -> Callable[[], bool]:
        def result() -> bool:
            fn()
            return False

        return result

    def ntsc() -> None:
        def impl() -> None:
            from edpu.pynput_ex import sleep

            c.press_delay('e')
            sleep()
            c.press_delay('r')
            sleep()
            c.press_delay('r')
            sleep()
            c.press_delay('n')

        c.alt_tab_wrap(lambda: c.key_wrap(Key.alt, impl))

    run(list(map(
        lambda elem: (f'\n\n{elem[0]}\n\n', get_false_returner(elem[1])),
        [
            ('LEFT', lambda: c.alt_tab_wrap(lambda: c.press_delay(Key.left))),
            ('RIGHT', lambda: c.alt_tab_wrap(lambda: c.press_delay(Key.right))),
            ('OPEN', lambda: [c.alt_tab(), c.key_wrap(Key.ctrl, lambda: c.press_delay('o'))]),
            ('NTSC', ntsc),
        ]
    )))
