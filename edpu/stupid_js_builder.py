def load_file(path: str) -> str:
    with open(path, encoding='ascii') as file:
        return file.read()


def load_module(path: str) -> str:
    from edpu_user.js import js_module_path
    return load_file(fr'{js_module_path()}\{path}')


def save_file(path: str, data: str) -> None:
    with open(path, 'w', encoding='ascii', newline='') as file:
        file.write(data)


def build_file(path: str, data: list[str]) -> None:
    save_file(path, '\n'.join(data))
