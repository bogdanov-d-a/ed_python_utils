from ..context_manager import DummyContextManager
from .string_utils import WrapDataData, WrapDataDataElem
from typing import Any, Optional


def get_pid_data() -> WrapDataDataElem:
    from os import getpid
    return ('getpid()', getpid())


def get_introduce_data(caller: str, name: Optional[str]=None) -> WrapDataData:
    from .string_utils import NAME, CALLER

    data: WrapDataData = [
        (CALLER, caller),
        get_pid_data(),
    ]

    if name is not None:
        data.append((NAME, name))

    return data


def wait_for_input(caller: str, print_lock: Any=DummyContextManager()) -> None:
    from .string_utils import wrap_data

    with print_lock:
        print(wrap_data(
            'wait_for_input',
            get_introduce_data(caller)
        ))

    input('waiting for input\n')
