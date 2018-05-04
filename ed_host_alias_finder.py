from socket import gethostname

def get_alias_from_map(alias_map):
    return alias_map.get(gethostname())
