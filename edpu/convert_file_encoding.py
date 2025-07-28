from typing import Optional


def convert_file_encoding(encoding_in: str, encoding_out: str, path_in: str, path_out: Optional[str]=None) -> None:
    if path_out is None:
        path_out = path_in

    def load() -> str:
        with open(path_in, encoding=encoding_in) as file:
            return file.read()

    def save(data: str) -> None:
        with open(path_out, 'w', encoding=encoding_out) as file:
            file.write(data)

    save(load())
