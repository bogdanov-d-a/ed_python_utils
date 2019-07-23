from subprocess import check_call

def validate_or_throw(var, var_name):
    if '"' in var:
        raise Exception(var_name + ' is invalid')

def encrypt(file_name, password, archive_name):
    validate_or_throw(file_name, 'file name')
    validate_or_throw(password, 'password')
    validate_or_throw(archive_name, 'archive name')
    check_call('7z a -mx1 -sdel -p"' + password + '" "' + archive_name + '" "' + file_name + '"')
