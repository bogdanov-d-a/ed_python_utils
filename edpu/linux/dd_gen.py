DD_GEN_DD = 'dd'


def dd_gen_if_of(if_: str, of_: str) -> list[str]:
    from ..string_utils import apostrophe_wrap

    return [
        f'if={apostrophe_wrap(if_)}',
        f'of={apostrophe_wrap(of_)}',
    ]


def dd_gen_bs_count(bs: str, count: str) -> list[str]:
    return [
        f'bs={bs}',
        f'count={count}',
    ]


def dd_gen_offset(offset: str, offset_type: str) -> str:
    return f'{offset_type}={offset}'


DD_GEN_OFFSET_TYPE_IF_SKIP = 'skip'
DD_GEN_OFFSET_TYPE_OF_SEEK = 'seek'


def dd_gen_status_progress() -> str:
    return 'status=progress'


DD_GEN_URANDOM = '/dev/urandom'


def dd_gen_wipe_dev(dev: str, bs: str, offset: str, count: str) -> str:
    from ..string_utils import merge_with_space

    return merge_with_space(
        [DD_GEN_DD]
        + dd_gen_if_of(DD_GEN_URANDOM, dev)
        + dd_gen_bs_count(bs, count)
        + [
            dd_gen_offset(offset, DD_GEN_OFFSET_TYPE_OF_SEEK),
            dd_gen_status_progress(),
        ]
    )
