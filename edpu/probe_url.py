UNKNOWN = 'UNKNOWN'
EMPTY = 'EMPTY'

HTTPS_PREFIX = 'https://'

WWW = 'www'
EN = 'en'
RU = 'ru'
ORG = 'org'
COM = 'com'

WIKIPEDIA = 'wikipedia'
YOUTUBE = 'youtube'
GITHUB = 'github'
STACKOVERFLOW = 'stackoverflow'
PYPI = 'pypi'


def wikipedia(url: str) -> list[str]:
    for domain in [
        WWW,
        EN,
        RU,
    ]:
        if url.startswith(f'{HTTPS_PREFIX}{domain}.{WIKIPEDIA}.{ORG}/'):
            return [
                WIKIPEDIA,
                domain,
            ]

    if url.startswith(f'{HTTPS_PREFIX}{WIKIPEDIA}.{ORG}/'):
        return [WIKIPEDIA]

    return []


def youtube(url: str) -> list[str]:
    if url.startswith(f'{HTTPS_PREFIX}{WWW}.{YOUTUBE}.{COM}/'):
        return [YOUTUBE]

    return []


def github(url: str) -> list[str]:
    if url.startswith(f'{HTTPS_PREFIX}{GITHUB}.{COM}/'):
        return [GITHUB]

    return []


def stackoverflow(url: str) -> list[str]:
    if url.startswith(f'{HTTPS_PREFIX}{STACKOVERFLOW}.{COM}/'):
        return [STACKOVERFLOW]

    return []


def pypi(url: str) -> list[str]:
    if url.startswith(f'{HTTPS_PREFIX}{PYPI}.{ORG}/'):
        return [PYPI]

    return []


def probe_url(url: str) -> list[str]:
    if url == '':
        return [EMPTY]

    result: list[str] = []

    if not url.startswith(HTTPS_PREFIX):
        result.append('Non-HTTPS address')

    result += wikipedia(url)
    result += youtube(url)
    result += github(url)
    result += stackoverflow(url)
    result += pypi(url)

    if len(result) == 0:
        return [UNKNOWN]

    return result
