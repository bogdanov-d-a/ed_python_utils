from typing import Optional


DD_GEN_DD = 'dd'


def dd_gen_if_of(if_: Optional[str], of_: Optional[str]) -> list[str]:
    from ..string_utils import apostrophe_wrap

    result = []

    if if_ is not None:
        result.append(f'if={apostrophe_wrap(if_)}')

    if of_ is not None:
        result.append(f'of={apostrophe_wrap(of_)}')

    return result


def dd_gen_bs_count(bs: str, count: str) -> list[str]:
    return [
        f'bs={bs}',
        f'count={count}',
    ]


def dd_gen_offset(offset: str, offset_type: str) -> str:
    return f'{offset_type}={offset}'


DD_GEN_OFFSET_TYPE_IF_SKIP = 'skip'
DD_GEN_OFFSET_TYPE_OF_SEEK = 'seek'


def dd_gen_iflag_fullblock() -> str:
    return 'iflag=fullblock'


def dd_gen_status_progress() -> str:
    return 'status=progress'


DD_GEN_URANDOM = '/dev/urandom'
DD_GEN_ZERO = '/dev/zero'


def dd_gen_zero(of_: Optional[str]=None) -> str:
    from ..string_utils import merge_with_space

    return merge_with_space(
        [DD_GEN_DD]
        + dd_gen_if_of(DD_GEN_ZERO, of_)
    )


def dd_gen_one() -> str:
    from ..string_utils import merge_with_space

    return merge_with_space(
        [DD_GEN_DD]
        + dd_gen_if_of(DD_GEN_ZERO, None)
        + [
            '|',
            r"tr '\0' '\377'",
        ]
    )


def dd_gen_wipe_dev(bs: str, offset: str, count: str, of_: Optional[str], if_: Optional[str]=DD_GEN_URANDOM) -> str:
    from ..string_utils import merge_with_space

    return merge_with_space(
        [DD_GEN_DD]
        + dd_gen_if_of(if_, of_)
        + dd_gen_bs_count(bs, count)
        + [
            dd_gen_iflag_fullblock(),
            dd_gen_offset(offset, DD_GEN_OFFSET_TYPE_OF_SEEK),
            dd_gen_status_progress(),
        ]
    )
