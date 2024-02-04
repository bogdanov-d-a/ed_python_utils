import traceback
from typing import Callable, Optional


DEFAULT_MESSAGE = 'Program completed successfully'


def run(f: Callable[[], None], wait_on_success: Optional[str]=None) -> None:
    try:
        f()
    except:
        wait_on_success = None
        traceback.print_exc()
        input()
    finally:
        if wait_on_success is not None:
            print(wait_on_success)
            input()
