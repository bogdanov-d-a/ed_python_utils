TYPE_DIR = 'dir'
TYPE_FILE = 'file'


def listdir_helper(root: str) -> dict[str, list[str]]:
    from os import listdir

    result: dict[str, list[str]] = { TYPE_DIR: [], TYPE_FILE: [] }

    for name in listdir(root):
        def get_type() -> str:
            from os.path import join, isfile, isdir

            path = join(root, name)

            if isfile(path):
                return TYPE_FILE

            if isdir(path):
                return TYPE_DIR

            raise Exception()

        result[get_type()].append(name)

    return result
