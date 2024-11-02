from typing import Callable


def pick_drive_windows() -> str:
    from edpu.win_device import physical_drive

    print('pick_drive_windows: INDEX (0, 1, ...)')
    index = input()

    return physical_drive(index)


def pick_drive_unix() -> str:
    print('pick_drive_unix: name (sda, sdb, ...)')
    name = input()

    return f'/dev/{name}'


def pick_profile() -> tuple[str, int]:
    from edpu.user_interaction import pick_str_option_ex

    return pick_str_option_ex('pick_profile', list(map(
        lambda profile: (profile[0], profile[1], (profile[1], profile[2])),
        [
            ('64g', '64 GB', 64*10**(3*3)),
            ('320g', '320 GB', 320*10**(3*3)),
            ('500g', '500 GB', 500*10**(3*3)),
            ('1t', '1 TB', 1*10**(3*4)),
            ('4t', '4 TB', 4*10**(3*4)),
        ]
    )))


def main(pick_drive: Callable[[], str]) -> None:
    from edpu.random_disk_reader import run

    drive = pick_drive()
    profile = pick_profile()

    run(profile[0], drive, 4096, profile[1], 1)


if __name__ == '__main__':
    from os import name
    main(pick_drive_windows if name == 'nt' else pick_drive_unix)
