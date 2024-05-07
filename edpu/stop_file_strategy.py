from __future__ import annotations


class StopFileStrategy:
    def __init__(self: StopFileStrategy, file_name: str) -> None:
        self._file_name = file_name


    def need_stop(self: StopFileStrategy) -> bool:
        from os.path import isfile
        return isfile(self._file_name)
