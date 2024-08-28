from typing import Optional


def mpv_va_detect(path: str, rev: Optional[bool]=None) -> tuple[str, str]:
    from .user_interaction import yes_no_prompt
    from os import listdir

    contents = listdir(path)

    if len(contents) != 2:
        raise Exception()

    print(contents)

    def rev_() -> bool:
        if rev is not None:
            return rev
        return yes_no_prompt('Reverse VA')

    return (contents[1], contents[0]) if rev_() else (contents[0], contents[1])


def mpv_play(va: tuple[str, str], path: str) -> None:
    from .popen_helper import popen_communicate_command_cwd
    from .string_utils import merge_with_space, quotation_mark_wrap
    from edpu_user.mpv import mpv_path

    v, a = va

    popen_communicate_command_cwd(merge_with_space([
        quotation_mark_wrap(mpv_path()),
        quotation_mark_wrap(v),
        quotation_mark_wrap(f'--audio-file={a}'),
    ]), path)


def mpv_va_detect_play(path: str, rev: Optional[bool]=None) -> None:
    mpv_play(mpv_va_detect(path, rev), path)
