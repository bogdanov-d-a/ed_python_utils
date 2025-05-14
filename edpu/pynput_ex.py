from __future__ import annotations
from pynput.keyboard import Controller, Key, KeyCode
from typing import Callable, Union


KeyT = Union[str, Key, KeyCode]
Fn = Callable[[], None]


def sleep() -> None:
    from time import sleep as impl
    impl(0.05)


class ControllerEx(Controller):
    def press_delay(self: ControllerEx, key: KeyT) -> None:
        self.press(key)
        sleep()
        self.release(key)


    def type_delay(self: ControllerEx, string: str) -> None:
        for char in string:
            sleep()
            self.press_delay(char)


    def key_wrap(self: ControllerEx, key: KeyT, fn: Fn) -> None:
        self.press(key)
        sleep()
        fn()
        sleep()
        self.release(key)


    def alt_tab(self: ControllerEx) -> None:
        self.key_wrap(Key.alt, lambda: self.press_delay(Key.tab))


    def alt_tab_wrap(self: ControllerEx, fn: Fn) -> None:
        self.alt_tab()
        sleep()
        fn()
        sleep()
        self.alt_tab()
