from __future__ import annotations


class DefFile:
    def __init__(self: DefFile, hash_: str, mtime: float) -> None:
        self.hash_ = hash_
        self.mtime = mtime

    def __eq__(self: DefFile, other: DefFile) -> bool:
        if isinstance(other, self.__class__):
            return self.hash_ == other.hash_ and self.mtime == other.mtime
        return False

    def save(self: DefFile, path: str) -> None:
        from codecs import open

        with open(path, 'w', 'utf-8-sig') as file:
            for str_ in [self.hash_, str(self.mtime)]:
                file.write(str_)
                file.write('\n')

    @staticmethod
    def load(path: str) -> DefFile:
        from codecs import open

        with open(path, 'r', 'utf-8-sig') as file:
            from ...string_utils import strip_crlf

            def non_empty(str_: str) -> str:
                str_ = strip_crlf(str_)
                if len(str_) == 0:
                    raise Exception()
                return str_

            hash_ = non_empty(file.readline())
            mtime = float(non_empty(file.readline()))

            if len(strip_crlf(file.readline())) != 0:
                raise Exception()

            return DefFile(hash_, mtime)
