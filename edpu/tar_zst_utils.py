TAR_ZST_EXT = '.tar.zst'


def pack_tar_zst(src_dir: str, dst_file: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap
    from edpu_user.m7z import f7z_path
    from edpu_user.zstd import zstd_path

    return merge_with_space([
        quotation_mark_wrap(f7z_path()),
        '-ttar',
        'a',
        'dummy',
        quotation_mark_wrap(src_dir),
        '-so',
        '|',
        quotation_mark_wrap(zstd_path()),
        '--fast',
        '-o',
        quotation_mark_wrap(dst_file + TAR_ZST_EXT),
    ])


def unpack_tar_zst(src_file: str, dst_dir: str) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap
    from edpu_user.m7z import f7z_path
    from edpu_user.zstd import zstd_path

    return merge_with_space([
        quotation_mark_wrap(zstd_path()),
        '-dc',
        quotation_mark_wrap(src_file + TAR_ZST_EXT),
        '|',
        quotation_mark_wrap(f7z_path()),
        'x',
        '-si',
        '-ttar',
        '-o' + quotation_mark_wrap(dst_dir),
    ])


def run_with_prompt(cmd: str) -> None:
    from .user_interaction import yes_no_prompt
    from subprocess import Popen

    print(cmd)

    if yes_no_prompt('Run command'):
        with Popen(cmd, shell=True) as process:
            process.communicate()


def print_and_check_path(path: str) -> None:
    from os.path import isfile, isdir

    if isfile(path):
        descr = 'file'
    elif isdir(path):
        descr = 'dir'
    else:
        descr = 'none'

    print(path + ' - ' + descr)
