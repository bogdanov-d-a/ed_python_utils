MOUNT_ROOT = '/mnt'


def mount_gen(device: str, dir: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        'mount',
        apostrophe_wrap(device),
        apostrophe_wrap(dir),
    ])


def umount_gen(dir: str) -> str:
    from ..string_utils import merge_with_space, apostrophe_wrap

    return merge_with_space([
        'umount',
        apostrophe_wrap(dir),
    ])


def mount_gen_advanced(device: str, dir_name: str) -> list[str]:
    from .utils_gen import cd, mkdir

    return [
        cd(MOUNT_ROOT),
        mkdir(dir_name),
        mount_gen(device, dir_name),
    ]


def umount_gen_advanced(dir_name: str) -> list[str]:
    from .utils_gen import cd

    return [
        cd(MOUNT_ROOT),
        umount_gen(dir_name),
    ]


def dir_name_to_mount_dir(dir_name: str) -> str:
    return MOUNT_ROOT + '/' + dir_name


def mount(device: str, dir_name: str) -> None:
    from os import mkdir, system
    from os.path import exists

    dir = dir_name_to_mount_dir(dir_name)

    if exists(dir):
        raise Exception(f'exists({dir})')

    mkdir(dir)
    system(mount_gen(device, dir))


def umount(dir_name: str) -> None:
    from os import rmdir, system

    dir = dir_name_to_mount_dir(dir_name)
    system(umount_gen(dir))
    rmdir(dir)
