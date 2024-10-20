def _parse(root_path: list[str], path: str) -> dict[str, str]:
    from ..impl.file_tree_snapshot import INDEX_PATH_SEPARATOR
    from codecs import open

    result: dict[str, str] = {}

    def result_add(name: str, comment: str) -> None:
        result[INDEX_PATH_SEPARATOR.join([INDEX_PATH_SEPARATOR.join(root_path), name])] = comment

    with open(path, 'r', 'utf-8-sig') as file:
        from ...string_utils import strip_crlf

        for line in list(map(strip_crlf, file.readlines())):
            if line[0] == '"':
                end = line.find('"', 1)

                if end == -1:
                    raise Exception('end == -1')

                if line[end + 1] != ' ':
                    raise Exception('line[end + 1] != \' \'')

                result_add(line[1:end], line[end + 2:])

            else:
                parts = line.split(' ', 1)

                if len(parts) != 2:
                    raise Exception('len(parts) != 2')

                result_add(parts[0], parts[1])

    return result


def _parse_all(data_path: str) -> dict[str, str]:
    from ..utils.file_tree_scanner import scan_descript_ion

    result: dict[str, str] = {}

    for rel_path in scan_descript_ion(data_path):
        from os import sep
        from os.path import join

        for path, comment in _parse(rel_path[:-1], join(data_path, sep.join(rel_path))).items():
            result[path] = comment

    return result


def _list_to_dict(data: list[tuple[str, str]]) -> dict[str, str]:
    result: dict[str, str] = {}

    for hash, comment in data:
        if hash in result:
            if result[hash] != comment:
                raise Exception(f'_list_to_dict conflict - discarded {hash} {comment}')
        else:
            result[hash] = comment

    return result


def _save_descript_ion_data(data: list[tuple[str, str]], file_path: str) -> None:
    from codecs import open

    with open(file_path, 'w', 'utf-8-sig') as output:
        from ..utils.utils import key_sorted_dict_items

        list_: list[tuple[str, str]] = key_sorted_dict_items(_list_to_dict(data))

        for hash, comment in list_:
            output.write(hash)
            output.write(' ')
            output.write(comment)
            output.write('\n')


def descript_ion_collect(data_path: str, common_data_path: str, descript_ion_path: str) -> None:
    from ..impl.definition import load_common_data_dict

    descript_ion = _parse_all(data_path)
    common_data = load_common_data_dict(common_data_path)

    mapped_data: list[tuple[str, str]] = []

    for path, comment in descript_ion.items():
        mapped_data.append((common_data[path], comment))

    _save_descript_ion_data(mapped_data, descript_ion_path)
