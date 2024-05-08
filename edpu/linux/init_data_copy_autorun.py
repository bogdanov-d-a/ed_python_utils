DIR_NAME = 'init_data'
TARGET_PATH = '/root'


def generate_file(path: str) -> None:
    with open(path, 'w', encoding='ascii', newline='') as file:
        from .archiso_bootmnt import archiso_bootmnt
        from .copy import copy_recursive
        from .shebang import SHEBANG_BIN_SH

        file.write(SHEBANG_BIN_SH + '\n')
        file.write(copy_recursive(f'{archiso_bootmnt()}/autorun/{DIR_NAME}', TARGET_PATH) + '\n')


def get_target_path() -> str:
    return f'{TARGET_PATH}/{DIR_NAME}'
