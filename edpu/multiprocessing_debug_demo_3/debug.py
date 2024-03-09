from __future__ import annotations
from . import mp_global as MPG
from enum import Enum, auto


class Mode(Enum):
    NONE = auto()
    MAIN = auto()
    WORKER = auto()


_mode = Mode.NONE


def worker_wait() -> bool:
    return _mode == Mode.WORKER


def worker(debug: bool, caller: str) -> None:
    if not worker_wait():
        return

    MPG.introduce_and_pop_pass(MPG.PmKey.DEBUG if debug else MPG.PmKey.WAIT, caller)


def main(caller: str) -> None:
    if _mode == Mode.MAIN:
        from ..concurrency_debug.utils import wait_for_input
        wait_for_input(caller)


def pass_managers(caller: str) -> None:
    if worker_wait():
        MPG.user_interaction_control(MPG.PmKey.DEBUG, caller)
        MPG.release(MPG.PmKey.WAIT, caller)
