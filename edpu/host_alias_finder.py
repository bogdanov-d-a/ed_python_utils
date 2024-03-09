def get_alias_from_map(alias_map: dict[str, str]) -> str:
    from socket import gethostname
    return alias_map[gethostname()]
