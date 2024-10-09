from __future__ import annotations


class App:
    def __init__(self: App, paths: list[str], suffixes: list[str], debug: bool=False) -> None:
        self.paths = paths
        self._suffixes = suffixes
        self._debug = debug


    def run(self: App) -> None:
        from .. import pause_at_end

        def impl() -> None:
            from .switcher import Switcher

            switcher = Switcher(self)

            active_suffix = switcher.get_active_suffix()
            print('active suffix is ' + active_suffix)

            new_suffix = self._pick_suffix()
            print('new suffix is ' + new_suffix)

            switcher.switch_to_suffix(active_suffix, new_suffix)

        pause_at_end.run(impl, pause_at_end.DEFAULT_MESSAGE)


    def get_suffix_paths(self: App) -> dict[str, list[str]]:
        return {
            suffix: list(map(lambda path_: path_ + suffix, self.paths))
            for suffix in self._suffixes
        }


    def rename(self: App, src: str, dst: str) -> None:
        from os.path import isdir, exists

        if not isdir(src):
            raise Exception('not isdir(src)')

        if exists(dst):
            raise Exception('exists(dst)')

        print('rename from ' + src + ' to ' + dst)

        if not self._debug:
            from os import rename as impl
            impl(src, dst)


    def _pick_suffix(self: App) -> str:
        from ..user_interaction import pick_str_option

        return pick_str_option('pick new suffix', {
            suffix: suffix
            for suffix in self._suffixes
        })
