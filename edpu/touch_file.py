def touch_file(path: str) -> None:
    from os.path import exists

    if exists(path):
        raise Exception(f'exists({path})')

    with open(path, 'wb'):
        pass
