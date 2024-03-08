from . import debug
from . import mp_global as MPG


def print_helper(thread: debug.Thread, location: debug.Location, key: int) -> None:
    with MPG.print_lock():
        print(f'print_helper {str((thread, location, key))}')


def trace_helper(thread: debug.Thread, location: debug.Location, key: int, count: int) -> None:
    from .trace import trace
    trace(str((thread, location, key)), count)


def worker1(key: int) -> None:
    debug.thread(debug.Thread.WORKER1, debug.Location.START, key)
    print_helper(debug.Thread.WORKER1, debug.Location.START, key)
    debug.before_fork(debug.Thread.WORKER1)

    with MPG.make_process_pool_executor(2) as executor:
        futures = list(map(
            lambda cmd: executor.submit(cmd[0], cmd[1]*10 + key),
            [(worker2_a, 1), (worker2_b, 2)]
        ))

        for future in futures:
            future.result()

    debug.thread(debug.Thread.WORKER1, debug.Location.END, key)
    print_helper(debug.Thread.WORKER1, debug.Location.END, key)


def worker2_a(key: int) -> None:
    debug.thread(debug.Thread.WORKER2_A, debug.Location.START, key)
    print_helper(debug.Thread.WORKER2_A, debug.Location.START, key)
    trace_helper(debug.Thread.WORKER2_A, debug.Location.START, key, 3)
    print_helper(debug.Thread.WORKER2_A, debug.Location.END, key)


def worker2_b(key: int) -> None:
    debug.thread(debug.Thread.WORKER2_B, debug.Location.START, key)
    print_helper(debug.Thread.WORKER2_B, debug.Location.START, key)
    trace_helper(debug.Thread.WORKER2_B, debug.Location.START, key, 5)
    print_helper(debug.Thread.WORKER2_B, debug.Location.END, key)


def main() -> None:
    debug.main(debug.Location.START)
    MPG.init(not debug.no_thread_wait())

    print_helper(debug.Thread.MAIN, debug.Location.START, 0)
    debug.before_fork(debug.Thread.MAIN)

    with MPG.make_process_pool_executor(4) as executor:
        futures = list(map(
            lambda key: executor.submit(worker1, key),
            range(4)
        ))

        debug.before_results_main()

        for future in futures:
            future.result()

    debug.main(debug.Location.END)
    print_helper(debug.Thread.MAIN, debug.Location.END, 0)
