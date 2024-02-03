from subprocess import check_call

def validate_or_throw(var: str, var_name: str) -> None:
    if '"' in var:
        raise Exception(var_name + ' is invalid')

def encrypt(file_name: str, password: str, archive_name: str) -> None:
    validate_or_throw(file_name, 'file name')
    validate_or_throw(password, 'password')
    validate_or_throw(archive_name, 'archive name')
    check_call('7z a -mx0 -sdel -p"' + password + '" "' + archive_name + '" "' + file_name + '"')
