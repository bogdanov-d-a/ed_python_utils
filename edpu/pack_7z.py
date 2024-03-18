S_7Z_EXT = '.7z'


def pack_7z(file_name: str, archive_name: str) -> None:
    from .string_utils import merge_with_space, quotation_mark_wrap
    from edpu_user.m7z import f7z_path
    from os.path import exists
    from subprocess import check_call

    if exists(archive_name):
        raise Exception('exists(archive_name)')

    check_call(merge_with_space([
        quotation_mark_wrap(f7z_path()),
        'a',
        '-mx0',
        quotation_mark_wrap(archive_name),
        quotation_mark_wrap(file_name),
    ]))
