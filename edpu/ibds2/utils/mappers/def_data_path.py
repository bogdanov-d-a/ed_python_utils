from .type_prefix import prefix_to_type, type_to_prefix


def def_path_to_data_path(def_path: list[str]) -> tuple[str, list[str]]:
    type_ = prefix_to_type(def_path[-1][0])
    data_path = list(map(lambda a: a[1:], def_path[:-1])) + [def_path[-1][1:]]
    return type_, data_path


def data_path_to_def_path(path_: list[str], type_: str) -> list[str]:
    return list(map(lambda a: '_' + a, path_[:-1])) + [type_to_prefix(type_) + path_[-1]]
