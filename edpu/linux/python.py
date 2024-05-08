def python() -> str:
    return 'python3'


def python_lib() -> str:
    from edpu_user.linux.python3 import python3_minor_version
    return f'/usr/lib/python3.{python3_minor_version()}'
