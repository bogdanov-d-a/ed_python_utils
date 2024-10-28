def bootstrap(path: str) -> None:
    with open(path, 'w', encoding='ascii', newline='') as file:
        from ..string_utils import merge_with_space, apostrophe_wrap
        from .init_data_copy_autorun import get_target_path
        from .shebang import SHEBANG_BIN_SH
        from .utils_gen import cd
        from typing import Optional

        file.write(SHEBANG_BIN_SH + '\n\n')

        file.write(merge_with_space([
            'chmod',
            '-R',
            '+x',
            apostrophe_wrap(get_target_path()),
        ]) + '\n')

        file.write(cd(get_target_path()) + '\n\n')

        modules: list[tuple[str, Optional[bool]]] = [
            ('edpu', False),
            ('edpu_local', True),
            ('edpu_user', None),
        ]

        for module, module_mode in modules:
            from .copy import copy_recursive
            from .python import python_lib
            from .rm import rm_rf

            if module_mode is not None:
                from .m7z import f7z_extract
                from .utils_gen import mkdir

                if module_mode:
                    file.write(mkdir(module) + '\n')
                    file.write(cd(module) + '\n')

                file.write(f7z_extract(f'{get_target_path()}/{module}.7z') + '\n')

                if module_mode:
                    file.write(cd('..') + '\n')

            file.write(copy_recursive(
                f'{get_target_path()}/{module}',
                python_lib()
            ) + '\n')

            file.write(rm_rf(
                f'{get_target_path()}/{module}',
            ) + '\n\n')
