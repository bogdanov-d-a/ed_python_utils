from __future__ import annotations
from ..concurrency_debug.multiprocessing.pass_manager import PassManager
from concurrent.futures import ProcessPoolExecutor
from enum import Enum, auto
from multiprocessing.synchronize import Lock
from typing import Optional


class PmKey(Enum):
    DEBUG = auto()
    WAIT = auto()


class Data:
    def __init__(self: Data, print_lock: Lock, pass_managers: Optional[dict[PmKey, PassManager]]) -> None:
        self.print_lock = print_lock
        self.pass_managers = pass_managers

    def get_pass_managers(self: Data) -> dict[PmKey, PassManager]:
        if self.pass_managers is None:
            raise Exception()
        return self.pass_managers


def set(value_: Data) -> None:
    global value
    value = value_


def get() -> Data:
    return value


def init(add_pass_managers: bool) -> None:
    from multiprocessing import Lock

    print_lock = Lock()
    pass_managers = None

    if add_pass_managers:
        pass_managers = {
            PmKey.DEBUG: PassManager('debug', print_lock),
            PmKey.WAIT: PassManager('wait', print_lock),
        }

    set(Data(print_lock, pass_managers))


def print_lock() -> Lock:
    return get().print_lock


def make_process_pool_executor(max_workers: int) -> ProcessPoolExecutor:
    return ProcessPoolExecutor(max_workers, initializer=set, initargs=(get(),))


def introduce_and_pop_pass(key: PmKey, caller: str) -> None:
    from ..concurrency_debug.multiprocessing.utils import introduce_and_pop_pass as impl
    impl(caller, get().get_pass_managers()[key], print_lock())


def user_interaction_control(key: PmKey, caller: str) -> None:
    get().get_pass_managers()[key].user_interaction_control(caller)


def release(key: PmKey, caller: str) -> None:
    get().get_pass_managers()[key].release(caller)
