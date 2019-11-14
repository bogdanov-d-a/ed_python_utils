import os

def create_dir_helper(root_dir, prefix):
    index = None

    while True:
        dir_name = prefix
        if index is not None:
            dir_name += "-" + str(index)
        dir_path = os.path.join(root_dir, dir_name)

        try:
            os.mkdir(dir_path)
            return dir_path
        except:
            pass

        if index is None:
            index = 0
        else:
            index += 1
