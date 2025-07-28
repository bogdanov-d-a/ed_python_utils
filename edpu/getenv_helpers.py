USERPROFILE = 'USERPROFILE'
APPDATA = 'APPDATA'
LOCALAPPDATA = 'LOCALAPPDATA'


def getenv_strict(key: str) -> str:
    from os import getenv
    result = getenv(key)

    if result is None:
        raise EnvironmentError(key)

    return result


def userprofile() -> str:
    return getenv_strict(USERPROFILE)


def appdata_roaming() -> str:
    return getenv_strict(APPDATA)


def appdata_local() -> str:
    return getenv_strict(LOCALAPPDATA)
