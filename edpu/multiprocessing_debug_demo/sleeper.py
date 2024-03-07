def sleeper(name: str) -> None:
    from time import sleep

    def print_helper(description: str) -> None:
        from ..concurrency_debug.string_utils import get_name_value
        from ..string_utils import merge_with_space
        from .mp_global import print_lock

        with print_lock():
            print(merge_with_space([
                'sleeper',
                description,
                get_name_value('name', name)
            ]))

    print_helper('start')
    sleep(1)
    print_helper('end')
