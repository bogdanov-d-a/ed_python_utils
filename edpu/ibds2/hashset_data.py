def save(data: set[str], path: str) -> None:
    with open(path, 'w') as file:
        for hash_ in sorted(data):
            file.write(hash_ + '\n')


def load(path: str) -> set[str]:
    from edpu.string_utils import strip_crlf
    from os.path import isfile

    if not isfile(path):
        return set()

    with open(path) as file:
        return set(map(strip_crlf, file.readlines()))
