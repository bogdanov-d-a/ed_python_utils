def _cmds() -> tuple[str, str]:
    #return ('gzip', 'gunzip')
    return ('pigz', 'unpigz')


def pack_cmd() -> str:
    return _cmds()[0] + ' -c -1'


def unpack_cmd() -> str:
    return _cmds()[1] + ' -c'
