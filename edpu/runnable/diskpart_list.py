if __name__ == '__main__':
    from edpu.string_utils import merge_with_newline
    from subprocess import run

    run(
        'diskpart',
        check=True,
        input=merge_with_newline(list(map(
            lambda item: f'list {item}',
            [
                'disk',
                'vdisk',
                'volume',
            ]
        ))),
        text=True
    )
