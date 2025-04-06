from typing import Optional


def start(args: list[str], path: Optional[str]=None, title: str='') -> str:
    from .string_utils import merge_with_space, quotation_mark_wrap

    data = [
        'start',
        quotation_mark_wrap(title),
    ]

    if path is not None:
        data += [
            '/d',
            quotation_mark_wrap(path),
        ]

    data += args

    return merge_with_space(data)
