from __future__ import annotations
from multiprocessing.synchronize import Lock
from typing import Any, Optional


class PassManager:
    def __init__(self: PassManager, name: str, print_lock: Lock) -> None:
        from ctypes import c_int
        from multiprocessing import Value

        self._name = name
        self._print_lock = print_lock

        self._passes = Value(c_int, 0)
        self._waiters = Value(c_int, 0)


    def get_name(self: PassManager) -> str:
        return self._name


    def release(self: PassManager, caller: str) -> None:
        with self._passes.get_lock():
            PassManager._set_value(self._passes, -1)
            self._print_helper('release', caller)


    def push_pass(self: PassManager) -> int:
        with self._passes.get_lock():
            if PassManager._get_value(self._passes) == -1:
                return -1

            return PassManager._increment_value(self._passes)


    def pop_pass_nowait(self: PassManager) -> tuple[bool, int]:
        with self._passes.get_lock():
            if PassManager._get_value(self._passes) == -1:
                return (True, -1)

            if PassManager._get_value(self._passes) > 0:
                return (True, PassManager._decrement_value(self._passes))

            return (False, PassManager._get_value(self._passes))


    def _pop_pass(self: PassManager, caller: str) -> None:
        while True:
            success, value = self.pop_pass_nowait()

            if success:
                self._print_helper(PassManager._pop_pass_name_helper('success'), caller, value)
                return

            from time import sleep
            sleep(2**-8)


    def pop_pass(self: PassManager, caller: str) -> None:
        from typing import Callable

        def handle_waiters(name: str, action: Callable[[Any], int]) -> None:
            with self._waiters.get_lock():
                self._print_helper(
                    PassManager._pop_pass_name_helper(name),
                    caller,
                    action(self._waiters)
                )

        handle_waiters('start', PassManager._increment_value)
        try:
            self._pop_pass(caller)
        finally:
            handle_waiters('end', PassManager._decrement_value)


    def user_interaction_control(self: PassManager, caller: str) -> None:
        from typing import Callable

        def get_action() -> Callable[[], None]:
            from ...user_interaction import pick_str_option_ex

            def exit() -> None:
                nonlocal stop
                stop = True

            PUSH_PASS = 'push_pass'
            POP_PASS_NOWAIT = 'pop_pass_nowait'

            return pick_str_option_ex(self._wrap_helper('user_interaction_control', caller), [
                ('a', PUSH_PASS, lambda: self._print_helper(PUSH_PASS, caller, self.push_pass())),
                ('r', POP_PASS_NOWAIT, lambda: self._print_helper(POP_PASS_NOWAIT, caller, self.pop_pass_nowait())),
                ('e', 'exit', exit),
            ], self._print_lock)

        try:
            stop = False

            while not stop:
                get_action()()

        finally:
            self.release(caller)


    def _wrap_helper(self: PassManager, outer: str, caller: Any, value: Optional[Any]=None) -> str:
        from ..string_utils import WrapDataData, wrap_data, NAME, CALLER, VALUE

        data: WrapDataData = [
            (NAME, self._name),
            (CALLER, caller),
        ]

        if value is not None:
            data.append((VALUE, value))

        return wrap_data(PassManager._class_name_helper(outer), data)


    def _print_helper(self: PassManager, outer: str, caller: Any, value: Optional[Any]=None) -> None:
        with self._print_lock:
            print(self._wrap_helper(outer, caller, value))


    @staticmethod
    def _class_name_helper(name: str) -> str:
        return f'PassManager {name}'


    @staticmethod
    def _pop_pass_name_helper(name: str) -> str:
        return f'pop_pass {name}'


    @staticmethod
    def _get_value(obj: Any) -> int:
        return obj.value


    @staticmethod
    def _set_value(obj: Any, value: int) -> None:
        obj.value = value


    @staticmethod
    def _increment_value(obj: Any) -> int:
        obj.value += 1
        return PassManager._get_value(obj)


    @staticmethod
    def _decrement_value(obj: Any) -> int:
        obj.value -= 1
        return PassManager._get_value(obj)
