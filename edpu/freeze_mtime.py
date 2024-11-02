def getmtime(path: str) -> float:
    from os.path import getmtime as impl
    return impl(path)


def setmtime(path: str, time: float) -> None:
    from os import utime
    utime(path, (time, time))


def freeze_mtime(path: str) -> None:
    try:
        from .user_interaction import yes_no_prompt_wait
        mtime = getmtime(path)
        yes_no_prompt_wait()

    finally:
        setmtime(path, mtime)
