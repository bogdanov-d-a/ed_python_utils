from socket import gethostname
from typing import Optional

def get_alias_from_map(alias_map: dict[str, str]) -> Optional[str]:
    return alias_map.get(gethostname())
