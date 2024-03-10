from typing import Optional


def load_line(path: str) -> Optional[str]:
    from os.path import exists

    if not exists(path):
        return None

    with open(path) as f:
        return f.readlines()[0].rstrip('\n')


def save_line(line: str, path: str) -> None:
    with open(path, 'w') as f:
        f.write(line)
