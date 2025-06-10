from typing import Optional


def _encode(char: str, encoding: str='utf-8') -> bytes:
    return char.encode(encoding)


def _encode_list(char_list: list[str], encoding: str='utf-8') -> list[bytes]:
    return list(map(
        lambda char: _encode(char, encoding),
        char_list
    ))


def _try_encode_list(char_list: list[str], encoding: str='utf-8') -> Optional[str]:
    try:
        _encode_list(char_list, encoding)
        return None

    except Exception as e:
        return str(e)


def str_check(str_: str) -> str:
    result = f'len(\'{str_}\') = {len(str_)}\n\n'

    str_list = list(str_)

    result += f'break = {str_list}\n\n'
    result += f'break_b = {_encode_list(str_list)}\n\n'

    str_set = sorted(set(str_list))

    result += f'set = {str_set}\n\n'
    result += f'set_b = {_encode_list(str_set)}\n\n'
    result += ('is ascii' if str_.isascii() else 'is *NOT* ascii') + '\n\n'

    def encoding_test() -> None:
        from .all_encodings import all_encodings

        for encoding in all_encodings():
            error = _try_encode_list(str_set, encoding)

            nonlocal result
            result += f'{encoding} = {'OK' if error is None else error}\n'

    encoding_test()

    return result
