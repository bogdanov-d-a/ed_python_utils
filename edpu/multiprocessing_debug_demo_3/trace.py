def trace(name: str, count: int) -> None:
    for i in range(count):
        from .mp_global import print_lock
        from time import sleep

        with print_lock():
            from ..concurrency_debug.string_utils import get_name_value, NAME, VALUE
            from ..string_utils import merge_with_space

            print(merge_with_space([
                'trace',
                get_name_value(NAME, name),
                get_name_value(VALUE, i),
            ]))

        sleep(1)
