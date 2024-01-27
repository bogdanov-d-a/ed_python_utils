import os

def open_dir_in_explorer(dir: str) -> None:
    os.system('explorer "' + dir + '"')
