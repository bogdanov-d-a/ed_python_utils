from typing import Optional


def batch_chcp_utf8() -> str:
    from .string_utils import merge_with_space

    return merge_with_space([
        'chcp',
        '65001',
    ])


def batch_chcp_utf8_nul() -> str:
    from .string_utils import merge_with_space

    return merge_with_space([
        batch_chcp_utf8(),
        '>',
        'NUL',
    ])


def batch_pipe_generate(command: str, out1: Optional[str], out2: Optional[str], out: str) -> None:
    from .string_utils import merge_with_space, quotation_mark_wrap

    with open(out, 'w', encoding='utf-8') as file:
        file.write(batch_chcp_utf8_nul() + '\n')

        data = [command]

        if out1 is not None:
            data += [
                '1>',
                quotation_mark_wrap(out1),
            ]

        if out2 is not None:
            data += [
                '2>',
                quotation_mark_wrap(out2),
            ]

        file.write(merge_with_space(data) + '\n')
