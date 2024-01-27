from .host_alias_finder import get_alias_from_map
from edpu_user import host_alias_map
from typing import Optional

def get() -> Optional[str]:
    return get_alias_from_map(host_alias_map.get())
