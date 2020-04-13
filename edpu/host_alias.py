from edpu.host_alias_finder import get_alias_from_map
import edpu_user.host_alias_map

def get():
    return get_alias_from_map(edpu_user.host_alias_map.get())
