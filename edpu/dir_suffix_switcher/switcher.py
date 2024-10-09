from __future__ import annotations
from .app import App


class Switcher:
    def __init__(self: Switcher, app: App) -> None:
        self._app = app
        self._suffix_paths = app.get_suffix_paths()


    def get_active_suffix(self: Switcher) -> str:
        from .utils import get_false_key, get_suffix_exists
        return get_false_key(get_suffix_exists(self._suffix_paths))


    def switch_to_suffix(self: Switcher, active_suffix: str, new_suffix: str) -> None:
        self._rename(active_suffix, True)
        self._rename(new_suffix, False)


    def _rename(self: Switcher, suffix: str, is_out: bool) -> None:
        for src, dst in zip(self._app.paths, self._suffix_paths[suffix]):
            if is_out:
                self._app.rename(src, dst)
            else:
                self._app.rename(dst, src)
