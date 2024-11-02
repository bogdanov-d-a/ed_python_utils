def _files() -> None:
    from os import getenv

    for path in [
        fr'{getenv("APPDATA")}\doublecmd',
        fr'{getenv("LOCALAPPDATA")}\doublecmd',
    ]:
        from os.path import isdir
        from shutil import rmtree

        if isdir(path):
            rmtree(path)


def main() -> None:
    _files()


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
