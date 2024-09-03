def _get_name(line: str) -> str:
    from re import match

    m = match(r'\S*', line)

    if m is None:
        raise Exception()

    return m[0]


def load_names(path: str) -> list[str]:
    with open(path, encoding='ascii') as file:
        return list(map(
            _get_name,
            file.readlines()[2:]
        ))


def pip_upgrade() -> str:
    return 'python -m pip install --upgrade pip'


def install(name: str) -> str:
    return pip_upgrade() if name == 'pip' else f'pip install {name}'


def upgrade(name: str) -> str:
    return pip_upgrade() if name == 'pip' else f'pip install {name} --upgrade --user'
