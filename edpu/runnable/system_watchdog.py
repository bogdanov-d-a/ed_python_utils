def _remove_file() -> None:
    from edpu.file_utils import remove_if_isfile
    from edpu_user.system_watchdog import system_watchdog_file_path, system_watchdog_file_path_bak
    from os import rename
    from os.path import isfile

    if not isfile(system_watchdog_file_path()):
        return

    remove_if_isfile(system_watchdog_file_path_bak())
    rename(system_watchdog_file_path(), system_watchdog_file_path_bak())


def _write_to_file(data: str) -> None:
    from edpu_user.system_watchdog import system_watchdog_file_path

    _remove_file()

    with open(system_watchdog_file_path(), 'w') as file:
        file.write(data)


def main() -> None:
    while True:
        from edpu.datetime_utils import get_now_datetime_str
        from edpu_user.system_watchdog import system_watchdog_file_name
        from time import sleep

        data = get_now_datetime_str()
        print(f'{system_watchdog_file_name()} - write_to_file - {data}')
        _write_to_file(data)
        sleep(60)


if __name__ == '__main__':
    main()
