from typing import Any, Callable, Optional, TypeVar


T = TypeVar('T')


def repeat_until_success(getter: Callable[[], T], on_exc: Callable[[Exception], Any], count: Optional[int]=None) -> T:
    if count is not None and count < 0:
        raise Exception('count is not None and count < 0')

    while True:
        try:
            return getter()

        except Exception as e:
            on_exc(e)

            if count == 0:
                raise e

            if count is not None:
                count -= 1
