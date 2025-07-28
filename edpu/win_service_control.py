from subprocess import CompletedProcess
from typing import Optional


SC = 'sc'

QUERY = 'query'
STOP = 'stop'


def run_sc(action: str, servicename: Optional[str]=None) -> CompletedProcess[bytes]:
    from subprocess import run

    data = [
        SC,
        action,
    ]

    if servicename is not None:
        data.append(servicename)

    return run(data)
