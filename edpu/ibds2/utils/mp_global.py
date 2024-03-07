from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from multiprocessing.synchronize import Lock


class Data:
    def __init__(self: Data, print_lock: Lock, data_lock: Lock) -> None:
        self.print_lock = print_lock
        self.data_lock = data_lock


def set(value_: Data) -> None:
    global value
    value = value_


def get() -> Data:
    return value


def init() -> None:
    from multiprocessing import Lock
    set(Data(Lock(), Lock()))


def print_lock() -> Lock:
    return get().print_lock


def data_lock() -> Lock:
    return get().data_lock


def make_process_pool_executor(max_workers: int) -> ProcessPoolExecutor:
    return ProcessPoolExecutor(max_workers, initializer=set, initargs=(get(),))
