def _load_descript_ion_data(file_path: str) -> dict[str, str]:
    from codecs import open

    with open(file_path, 'r', 'utf-8-sig') as input_:
        data_: dict[str, str] = {}

        for line in input_.readlines():
            if line[-1] == '\n':
                line = line[:-1]

            parts = line.split(' ', 1)

            if len(parts) != 2:
                raise Exception('len(parts) != 2')

            data_[parts[0]] = parts[1]

        return data_


def _generate_files_data(data: list[tuple[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}

    for path, comment in data:
        from ..impl.file_tree_snapshot import INDEX_PATH_SEPARATOR

        path = path.split(INDEX_PATH_SEPARATOR)

        path_root = path[:-1]
        path_name = path[-1]

        path_root_key = INDEX_PATH_SEPARATOR.join(path_root)

        if path_root_key not in result:
            result[path_root_key] = {}

        result[path_root_key][path_name] = comment

    return result


def _save_descript_ion_data(data: list[tuple[str, str]], data_path: str) -> None:
    for path_root_key, files_data in _generate_files_data(data).items():
        from ..impl.file_tree_snapshot import INDEX_PATH_SEPARATOR
        from ..utils.utils import DESCRIPT_ION
        from codecs import open
        from os.path import sep, join

        with open(join(data_path, sep.join(path_root_key.split(INDEX_PATH_SEPARATOR)), DESCRIPT_ION), 'w', 'utf-8-sig') as file:
            for name, comment in files_data.items():
                name_ = name if name.find(' ') == -1 else f'"{name}"'
                file.write(f'{name_} {comment}\r\n')


def descript_ion_apply(data_path: str, common_data_path: str, descript_ion_path: str) -> None:
    from ..impl.definition import load_common_data_dict

    descript_ion = _load_descript_ion_data(descript_ion_path)
    common_data = load_common_data_dict(common_data_path)

    mapped_data: list[tuple[str, str]] = []

    for path, hash in common_data.items():
        if hash in descript_ion:
            mapped_data.append((path, descript_ion[hash]))

    _save_descript_ion_data(mapped_data, data_path)
