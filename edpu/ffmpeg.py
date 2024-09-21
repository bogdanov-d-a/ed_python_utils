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


def ffmpeg_key(key: str) -> str:
    return f'-{key}'


def ffmpeg_keys(keys: list[str]) -> list[str]:
    return list(map(ffmpeg_key, keys))


def ffmpeg_input(input: list[str]) -> list[str]:
    from .string_utils import quotation_mark_wrap

    result = []

    for input_elem in input:
        result += ['-i', quotation_mark_wrap(input_elem)]

    return result


def ffmpeg_copy() -> list[str]:
    return [
        '-c',
        'copy',
    ]


def ffmpeg_gen(app_name: str, args: list[str]=[]) -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap
    return merge_with_space([quotation_mark_wrap(fr'{bin_path()}\{app_name}{EXE_EXT}')] + args)


def ffmpeg_cut(ss: str, to: str, input: list[str], output: str, accurate: bool=True) -> str:
    from .string_utils import quotation_mark_wrap

    span = [
        '-ss',
        ss,
        '-to',
        to,
    ]

    return ffmpeg_gen(
        FFMPEG,
        (ffmpeg_input(input) + span if accurate else span + ffmpeg_input(input)) + ffmpeg_copy() + [quotation_mark_wrap(output)]
    )


def ffmpeg_merge(input: list[str], output: str) -> str:
    from .string_utils import quotation_mark_wrap

    return ffmpeg_gen(
        FFMPEG,
        ffmpeg_input(input) + ffmpeg_copy() + [quotation_mark_wrap(output)]
    )
