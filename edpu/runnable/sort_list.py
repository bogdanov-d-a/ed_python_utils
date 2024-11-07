list_ = [
    'ghi',
    'abc',
    'def',
]


if __name__ == '__main__':
    for elem in sorted(list_):
        from edpu.string_utils import apostrophe_wrap
        print(' ' * 4 * 1 + apostrophe_wrap(elem) + ',')

    input()
