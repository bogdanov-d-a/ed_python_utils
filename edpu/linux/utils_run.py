def lsblk() -> None:
    from os import system
    system(f'lsblk')


def sync() -> None:
    from os import system
    system(f'sync')


def drop_caches() -> None:
    from os import system
    system(f'echo 3 | tee /proc/sys/vm/drop_caches')
