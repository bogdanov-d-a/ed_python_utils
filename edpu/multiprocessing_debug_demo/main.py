from . import debug
from . import mp_global as MPG


def print_helper(caller: debug.Mode) -> None:
    with MPG.print_lock():
        print(f'print_helper {str(caller)}')


def sleeper_helper(caller: debug.Mode) -> None:
    from .sleeper import sleeper
    sleeper(str(caller))


def a():
    debug.thread(debug.Mode.A_START)
    sleeper_helper(debug.Mode.A_START)


def b():
    debug.thread(debug.Mode.B_START)
    sleeper_helper(debug.Mode.B_START)


def c():
    debug.thread(debug.Mode.C_START)
    sleeper_helper(debug.Mode.C_START)


def d():
    debug.thread(debug.Mode.D_START)
    sleeper_helper(debug.Mode.D_START)


def cd():
    debug.thread(debug.Mode.CD_START)
    print_helper(debug.Mode.CD_START)
    debug.before_fork(debug.Mode.CD_START)

    with MPG.make_process_pool_executor(2) as executor:
        futures = list(map(
            executor.submit,
            [c, d]
        ))

        for future in futures:
            future.result()

    debug.thread(debug.Mode.CD_END)
    print_helper(debug.Mode.CD_END)


def main() -> None:
    debug.main(debug.Mode.MAIN_START)
    MPG.init()
    debug.before_fork(debug.Mode.MAIN_START)

    with MPG.make_process_pool_executor(3) as executor:
        futures = list(map(
            executor.submit,
            [a, b, cd]
        ))

        debug.before_results_main()

        for future in futures:
            future.result()

    debug.main(debug.Mode.MAIN_END)
    print_helper(debug.Mode.MAIN_END)
