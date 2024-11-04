from typing import Any, Callable


def log_watcher(path: str, lines: int, waiter: Callable[[], Any]) -> None:
    while True:
        from edpu.user_interaction import accent_print

        with open(path, encoding='utf-8') as file:
            from edpu.string_utils import strip_crlf

            for line in list(map(
                strip_crlf,
                file.readlines()[-lines:]
            )):
                print(line)

        accent_print(['Ready to reload file'])
        waiter()
