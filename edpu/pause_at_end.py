from typing import Any, Callable, Optional


DEFAULT_MESSAGE = 'Program completed successfully'


def run(f: Callable[[], Any], wait_on_success: Optional[str]=None) -> None:
    try:
        f()

    except:
        from traceback import print_exc

        wait_on_success = None
        print_exc()
        input()

    finally:
        if wait_on_success is not None:
            print(wait_on_success)
            input()
