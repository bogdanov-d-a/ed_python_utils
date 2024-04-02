def _rmtree(path: str) -> None:
    from os.path import isdir
    from shutil import rmtree

    if isdir(path):
        rmtree(path)


def _remove(path: str) -> None:
    from os import remove
    from os.path import isfile

    if isfile(path):
        remove(path)


def _files() -> None:
    from os import getenv

    up = getenv('USERPROFILE')
    adl = getenv('LOCALAPPDATA')

    _rmtree(fr'{up}\.cache')
    _rmtree(fr'{up}\.idlerc')

    _remove(fr'{up}\.bash_history')

    _rmtree(fr'{adl}\cache')

    _remove(fr'{adl}\IconCache.db')
    _remove(fr'{adl}\recently-used.xbel')


def main() -> None:
    _files()


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
