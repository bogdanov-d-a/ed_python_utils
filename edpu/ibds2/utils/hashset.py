def save(data: set[str], path: str) -> None:
    with open(path, 'w') as file:
        for hash_ in sorted(data):
            file.write(hash_ + '\n')


def load(path: str) -> set[str]:
    from os.path import isfile

    if not isfile(path):
        return set()

    with open(path) as file:
        from ...string_utils import strip_crlf
        return set(map(strip_crlf, file.readlines()))
