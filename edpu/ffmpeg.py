from typing import Optional


def bin_path() -> str:
    from edpu_user.ffmpeg import ffmpeg_path
    return fr'{ffmpeg_path()}\bin'


EXE_EXT = '.exe'

FFMPEG = 'ffmpeg'
FFPLAY = 'ffplay'
FFPROBE = 'ffprobe'


FFPROBE_KEYS = [
    'unit',
    'prefix',
    'sexagesimal',
    'show_data',
    'show_data_hash CRC32',
    'show_error',
    'show_format',
    #'show_frames',
    #'show_packets',
    'show_programs',
    'show_streams',
    'show_chapters',
    'count_frames',  # slow
    'count_packets',
    #'show_pixel_formats',
    'show_private_data',
    #'bitexact',  # uninformative
]


def ffmpeg_gen(app_name: str, keys: list[str]=[], path: Optional[str]=None) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    data = [quotation_mark_wrap(fr'{bin_path()}\{app_name}{EXE_EXT}')]

    data += list(map(
        lambda key: f'-{key}',
        keys
    ))

    if path is not None:
        data.append(quotation_mark_wrap(path))

    return merge_with_space(data)
