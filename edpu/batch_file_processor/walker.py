from typing import Callable


def walk(src_dir: str, dst_dir: str, processor: Callable[[str], None]) -> None:
    from edpu.guided_directory_use import PathKeeper
    from os.path import exists

    if not exists(src_dir):
        raise Exception('not exists(src_dir)')

    with PathKeeper(dst_dir):
        from os import listdir

        for src_name in listdir(src_dir):
            try:
                processor(src_name)

            except:
                print('Error: ' + src_name)

        if len(listdir(src_dir)) != 0:
            print('src_dir is not empty')
            input()
