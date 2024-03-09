from . import debug
from . import mp_global as MPG
from .trace import trace


def worker1(key: int) -> None:
    MPG.print_with_lock(f'worker1 start {key}')

    with MPG.make_process_pool_executor(2) as executor:
        futures = list(map(
            lambda cmd: executor.submit(cmd[0], cmd[1]*10 + key),
            [(worker2_a, 1), (worker2_b, 2)]
        ))

        for future in futures:
            future.result()

    MPG.print_with_lock(f'worker1 end {key}')


def worker2_a(key: int) -> None:
    MPG.print_with_lock(f'worker2_a start {key}')
    trace(f'worker2_a {key}', 3)
    MPG.print_with_lock(f'worker2_a end {key}')


def worker2_b(key: int) -> None:
    MPG.print_with_lock(f'worker2_b start {key}')
    trace(f'worker2_b {key}', 5)
    MPG.print_with_lock(f'worker2_b end {key}')


def main() -> None:
    debug.main(f'main start')
    MPG.init(debug.worker_wait())
    MPG.print_with_lock(f'main start')

    with MPG.make_process_pool_executor(4) as executor:
        futures = list(map(
            lambda key: executor.submit(worker1, key),
            range(4)
        ))

        debug.pass_managers(f'main process_pool_executor')

        for future in futures:
            future.result()

    MPG.print_with_lock(f'main end')
