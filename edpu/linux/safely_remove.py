def safely_remove(device: str) -> None:
    from ..user_interaction import user_wait
    from .utils_run import lsblk, sync
    from os import system

    user_wait('umount')
    lsblk()
    user_wait('stop using drive')
    sync()
    user_wait('wait for ~10 seconds')
    system(f'hdparm -Y /dev/{device}')
    user_wait('wait for ~10 seconds')
    system(f'echo 1 | tee /sys/block/{device}/device/delete')
    lsblk()
    user_wait('wait for ~10 seconds')
    user_wait('physically detach drive')
