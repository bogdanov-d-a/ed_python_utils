import os

def open_dir_in_explorer(dir):
    os.system('explorer "' + dir + '"')
