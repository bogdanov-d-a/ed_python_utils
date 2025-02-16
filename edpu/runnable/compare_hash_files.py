def get_args_filenames() -> tuple[str, str]:
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('a')
    parser.add_argument('b')
    args = parser.parse_args()

    return (args.a, args.b)


if __name__ == '__main__':
    from edpu.compare_hash_files import run

    a, b = get_args_filenames()
    run(a, b)
