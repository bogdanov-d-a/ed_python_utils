from . import mp_global as MPG
from enum import Enum, auto


class Mode(Enum):
    NONE = auto()
    MAIN_START = auto()
    MAIN_END = auto()
    A_START = auto()
    B_START = auto()
    CD_START = auto()
    CD_END = auto()
    C_START = auto()
    D_START = auto()


mode = Mode.NONE


def no_thread_wait() -> bool:
    return mode in [Mode.NONE, Mode.MAIN_END]


def cd_forks() -> list[Mode]:
    return [Mode.C_START, Mode.D_START]


def thread(caller: Mode) -> None:
    if caller in [Mode.NONE, Mode.MAIN_START, Mode.MAIN_END]:
        raise Exception()

    if no_thread_wait():
        return

    if caller == Mode.CD_START and mode in cd_forks():
        return

    if mode == Mode.CD_END and caller in [Mode.CD_START] + cd_forks():
        return

    MPG.introduce_and_pop_pass(
        MPG.PmKey.DEBUG if mode == caller else MPG.PmKey.WAIT,
        str(caller)
    )


def main(caller: Mode) -> None:
    if caller not in [Mode.MAIN_START, Mode.MAIN_END]:
        raise Exception()

    if mode == caller:
        from ..concurrency_debug.utils import wait_for_input
        wait_for_input(str(caller))


def before_fork(caller: Mode) -> None:
    if mode == caller:
        raise Exception('before_fork')


def before_results_main() -> None:
    if not no_thread_wait():
        CALLER = 'before_results_main'
        MPG.user_interaction_control(MPG.PmKey.DEBUG, CALLER)
        MPG.release(MPG.PmKey.WAIT, CALLER)
