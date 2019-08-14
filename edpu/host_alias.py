from ed_host_alias_finder import get_alias_from_map
import ed_host_alias_map

def get():
    return get_alias_from_map(ed_host_alias_map.get())
