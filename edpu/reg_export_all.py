def reg_export_all(keys: list[tuple[str, list[str]]], root: str) -> None:
    for key, strip_prefixes in keys:
        from .win_reg import reg_export
        from .win_reg_strip import win_reg_strip
        from os.path import join

        path = join(root, key + '.reg')
        reg_export(key, path, True)
        win_reg_strip(strip_prefixes, path)
