from .pass_manager import PassManager
from typing import Any


def introduce_and_pop_pass(caller: str, pass_manager: PassManager, print_lock: Any) -> None:
    from ..string_utils import wrap_data
    from ..utils import get_introduce_data

    with print_lock:
        print(wrap_data(
            'introduce_and_pop_pass',
            get_introduce_data(caller, pass_manager.get_name())
        ))

    pass_manager.pop_pass(caller)
