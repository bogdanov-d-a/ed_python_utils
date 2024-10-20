def save_common_data(common_data: list[tuple[str, str]], file_path: str) -> None:
    from codecs import open

    with open(file_path, 'w', 'utf-8-sig') as output:
        for path, hash_ in common_data:
            output.write(hash_)
            output.write(' ')
            output.write(path)
            output.write('\n')


def load_common_data(file_path: str) -> list[tuple[str, str]]:
    from codecs import open

    with open(file_path, 'r', 'utf-8-sig') as input_:
        data_: list[tuple[str, str]] = []

        for line in input_.readlines():
            if line[-1] == '\n':
                line = line[:-1]

            parts = line.split(' ', 1)

            if len(parts) != 2:
                raise Exception('load_common_data bad format')

            data_.append((parts[1], parts[0]))

        return data_


def load_common_data_dict(file_path: str) -> dict[str, str]:
    return {
        path: hash
        for path, hash
        in load_common_data(file_path)
    }


def save_hashset_data(hashset_data: set[str], file_path: str) -> None:
    from codecs import open

    with open(file_path, 'w', 'utf-8-sig') as output:
        for hash_ in sorted(list(hashset_data)):
            output.write(hash_)
            output.write('\n')
