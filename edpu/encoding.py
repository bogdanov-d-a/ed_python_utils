from typing import Optional


def check_ascii_file(filename: str) -> None:
    with open(filename, 'rb') as file:
        from .read_in_chunks import read_in_chunks

        for data in read_in_chunks(file):
            data.decode('ascii')


def decode_file(filename: str, encoding: str) -> str:
    with open(filename, 'rb') as file:
        return file.read().decode(encoding)


LINE_BREAK_CR = b'\r'
LINE_BREAK_LF = b'\n'

LINE_BREAK_WINDOWS = LINE_BREAK_CR + LINE_BREAK_LF
LINE_BREAK_UNIX = LINE_BREAK_LF
LINE_BREAK_MAC = LINE_BREAK_CR

LINE_BREAK_TYPES = [
    LINE_BREAK_WINDOWS,
    LINE_BREAK_UNIX,
    LINE_BREAK_MAC,
]


def line_break_types_count(filename: str) -> dict[bytes, int]:
    result: dict[bytes, int] = {}

    with open(filename, 'rb') as file:
        data = file.read()

        for line_break_type in LINE_BREAK_TYPES:
            result[line_break_type] = data.count(line_break_type)

    return result


def line_break_type(filename: str) -> Optional[bytes]:
    count = line_break_types_count(filename)

    if count[LINE_BREAK_WINDOWS] == count[LINE_BREAK_UNIX] == count[LINE_BREAK_MAC] == 0:
        return b''

    if count[LINE_BREAK_WINDOWS] == count[LINE_BREAK_UNIX] == count[LINE_BREAK_MAC]:
        return LINE_BREAK_WINDOWS

    if count[LINE_BREAK_WINDOWS] == count[LINE_BREAK_MAC] == 0 and count[LINE_BREAK_UNIX] > 0:
        return LINE_BREAK_UNIX

    if count[LINE_BREAK_WINDOWS] == count[LINE_BREAK_UNIX] == 0 and count[LINE_BREAK_MAC] > 0:
        return LINE_BREAK_MAC

    return None


def line_break_type_to_string(type: Optional[bytes]) -> str:
    return {
        b'': 'UNDEF',
        LINE_BREAK_WINDOWS: 'WIN',
        LINE_BREAK_UNIX: 'UNIX',
        LINE_BREAK_MAC: 'MAC',
        None: 'MIX',
    }[type]
