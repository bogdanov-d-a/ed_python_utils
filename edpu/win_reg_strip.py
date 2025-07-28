from __future__ import annotations
from .win_reg import DEFAULT_ENCODING
from typing import Callable, Optional


HEADER = '\ufeffWindows Registry Editor Version 5.00'


Value = list[str]
Values = list[Value]


class ValuesData:
    def __init__(self: ValuesData) -> None:
        self.values: Values = []
        self.value: Value = []


    def flush_value(self: ValuesData) -> None:
        if len(self.value) != 0:
            self.values.append(self.value)

        self.value = []


    def append_value_line(self: ValuesData, value_line: str) -> None:
        self.value.append(value_line)


class KeyData:
    def __init__(self: KeyData, name: str, exclude: bool) -> None:
        self.name = name
        self.values = None if exclude else ValuesData()


    def run_if_values_set(self: KeyData, fn: Callable[[ValuesData], None]) -> None:
        if self.values is not None:
            fn(self.values)


Keys = dict[str, Values]


class KeysData:
    def __init__(self: KeysData, prefixes: list[str]) -> None:
        from .trie import make_trie

        self.trie = make_trie(prefixes)
        self.keys: Keys = {}
        self.key = None


    def run_if_key_and_values_set(self: KeysData, fn: Callable[[KeyData, ValuesData], None]) -> None:
        if self.key is not None:
            key = self.key
            key.run_if_values_set(lambda values: fn(key, values))


    def flush_key(self: KeysData) -> None:
        def fn(key: KeyData, values: ValuesData) -> None:
            if key.name in self.keys:
                raise Exception()

            values.flush_value()
            self.keys[key.name] = values.values

        self.run_if_key_and_values_set(fn)
        self.key = None


    def process_key(self: KeysData, key: str) -> None:
        from .trie import in_trie

        self.flush_key()

        self.key = KeyData(
            key,
            in_trie(self.trie, key) or in_trie(self.trie, key + '\\', True)
        )


    def process_value_line(self: KeysData, line: str) -> None:
        if self.key is None:
            raise Exception()

        def fn(_: KeyData, values: ValuesData) -> None:
            if line.startswith('@') or line.startswith('"'):
                values.flush_value()

            values.append_value_line(line)

        self.run_if_key_and_values_set(fn)


def win_reg_strip(
    prefixes: list[str],
    path_in: str,
    path_out: Optional[str]=None,
    encoding_in: str=DEFAULT_ENCODING,
    encoding_out: str='utf-8'
) -> None:
    if path_out is None:
        path_out = path_in


    def read_and_filter() -> Keys:
        with open(path_in, encoding=encoding_in) as file:
            start = True
            keys = KeysData(prefixes)

            while True:
                from .string_utils import strip_crlf

                line = file.readline()
                eof = line == ''
                line = strip_crlf(line)

                if start:
                    if eof:
                        raise Exception()

                    if line != HEADER:
                        raise Exception()

                    start = False

                else:
                    if eof:
                        keys.flush_key()
                        return keys.keys

                    if len(line) != 0:
                        if line[0] == '[' and line[-1] == ']':
                            keys.process_key(line[1:-1])
                        else:
                            keys.process_value_line(line)


    def sort_and_write(keys: Keys) -> None:
        with open(path_out, 'w', encoding=encoding_out) as file:
            file.write(HEADER + '\n\n')

            for key, values in sorted(keys.items()):
                file.write(f'[{key}]\n')

                for value in sorted(values):
                    for value_line in value:
                        file.write(value_line + '\n')

                file.write('\n')


    sort_and_write(read_and_filter())
