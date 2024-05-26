BACKSLASH = '\\'
PREFIX = BACKSLASH + BACKSLASH + '.' + BACKSLASH


def physical_drive(index: str) -> str:
    return f'{PREFIX}PhysicalDrive{index}'


def drive_letter(letter: str) -> str:
    return f'{PREFIX}{letter}:'
