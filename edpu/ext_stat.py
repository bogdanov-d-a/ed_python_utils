def ext_stat(root: str) -> None:
    def stat() -> dict[str, int]:
        from os import listdir

        result: dict[str, int] = {}

        for name in listdir(root):
            from os.path import join, isfile, splitext

            if not isfile(join(root, name)):
                print(f'SKIPPED - {name}')
                continue

            ext = splitext(name)[1]

            if ext not in result:
                result[ext] = 0

            result[ext] += 1

        return result

    def impl() -> None:
        print(f'root - {root}')

        for ext, count in sorted(stat().items()):
            print(f'<{ext}> : {count}')

    impl()
