from typing import Callable


def read_file_text(path: str) -> str:
    with open(path, encoding='utf-8') as file:
        return file.read()


def write_text_to_file(text: str, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)


def input_to_output_file_conv(input: str, output: str, fn: Callable[[str], str]) -> None:
    write_text_to_file(
        fn(read_file_text(input)),
        output
    )
