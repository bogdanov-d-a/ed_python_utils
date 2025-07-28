UNKNOWN = 'UNKNOWN'


def find_drive(storage_hacks: dict[str, str]) -> None:
    from .favorite_dirs_manager import run
    from .storage_finder import get_drive_letters, find_all_storage

    drive_letters = sorted(set(get_drive_letters()))

    all_storage = {
        drive_letter: alias
        for alias, drive_letter
        in find_all_storage().items()
    }

    def drive_letter_description(drive_letter: str) -> str:
        alias = all_storage.get(
            drive_letter,
            storage_hacks.get(
                drive_letter,
                UNKNOWN
            )
        )

        return f'{alias} ({drive_letter[:-1]})'

    for drive_letter in drive_letters:
        print(drive_letter_description(drive_letter))

        from os import system
        system(f'vol {drive_letter[:-1]}')

        print()

    run('find_drive', list(map(
        lambda drive_letter: (
            drive_letter[:1].lower(),
            drive_letter_description(drive_letter),
            drive_letter
        ),
        drive_letters
    )))
