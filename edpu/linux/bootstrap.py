def bootstrap() -> None:
    from ..string_utils import merge_with_space, apostrophe_wrap
    from .init_data_copy_autorun import get_target_path
    from .utils_gen import cd
    from typing import Optional

    print(merge_with_space([
        'chmod',
        '-R',
        '+x',
        apostrophe_wrap(get_target_path()),
    ]))

    print(cd(get_target_path()))

    print()

    modules: list[tuple[str, Optional[bool]]] = [
        ('edpu', False),
        ('edpu_local', True),
        ('edpu_user', None),
    ]

    for module, module_mode in modules:
        from .copy import copy_recursive
        from .python import python_lib

        if module_mode is not None:
            from .m7z import f7z_extract
            from .utils_gen import mkdir

            if module_mode:
                print(mkdir(module))
                print(cd(module))

            print(f7z_extract(f'{get_target_path()}/{module}.7z'))

            if module_mode:
                print(cd('..'))

        print(copy_recursive(
            f'{get_target_path()}/{module}',
            python_lib()
        ))

        print()
