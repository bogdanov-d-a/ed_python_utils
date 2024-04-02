def path_join(a: str, b: str) -> str:
    from os.path import join
    return join(a, b)


def get_ext(name: str) -> str:
    from os.path import splitext
    return splitext(name)[1]


def remove_ext(name: str) -> str:
    from os.path import splitext
    return splitext(name)[0]
