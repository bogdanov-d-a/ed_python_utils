def generate_file(password: str, path: str) -> None:
    with open(path, 'w', encoding='ascii', newline='') as file:
        from ..string_utils import merge_with_space, apostrophe_wrap
        from .root import root
        from .shebang import SHEBANG_BIN_SH

        file.write(SHEBANG_BIN_SH + '\n')

        file.write(merge_with_space([
            'systemctl',
            'stop',
            'iptables',
        ]) + '\n')

        file.write(merge_with_space([
            'echo',
            apostrophe_wrap(f'{root()}:{password}'),
            '|',
            'chpasswd',
        ]) + '\n')
