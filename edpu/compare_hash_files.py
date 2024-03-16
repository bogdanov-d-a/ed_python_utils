def _read_file(path: str) -> str:
    with open(path) as file:
        from .string_utils import strip_crlf
        return strip_crlf(file.readline())


def run(a: str, b: str) -> None:
    from .string_utils import merge_with_space, apostrophe_wrap

    ah = _read_file(a)
    bh = _read_file(b)

    suffix = merge_with_space([
        'for',
        apostrophe_wrap(a),
        'and',
        apostrophe_wrap(b),
    ])

    if ah == bh:
        print(f'OK, same hash: {ah} {suffix}')

    else:
        print(f'FAIL, different hashes: {ah} and {bh} {suffix}')
