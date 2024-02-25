_INDEX_PATH_SEPARATOR = '\\'


def path_to_key(path: list[str]) -> str:
    return _INDEX_PATH_SEPARATOR.join(path)


def key_to_path(key: str) -> list[str]:
    return key.split(_INDEX_PATH_SEPARATOR)
