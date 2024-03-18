def validate_or_throw(var: str, var_name: str) -> None:
    if '"' in var:
        raise Exception(var_name + ' is invalid')

def encrypt(file_name: str, password: str, archive_name: str) -> None:
    from .string_utils import merge_with_space, quotation_mark_wrap
    from edpu_user.m7z import f7z_path
    from subprocess import check_call

    validate_or_throw(file_name, 'file name')
    validate_or_throw(password, 'password')
    validate_or_throw(archive_name, 'archive name')

    check_call(merge_with_space([
        quotation_mark_wrap(f7z_path()),
        'a',
        '-mx0',
        '-sdel',
        '-p' + quotation_mark_wrap(password),
        quotation_mark_wrap(archive_name),
        quotation_mark_wrap(file_name),
    ]))
