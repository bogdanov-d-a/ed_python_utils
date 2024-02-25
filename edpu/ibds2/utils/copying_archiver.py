from __future__ import annotations
from io import BufferedReader, BufferedWriter, TextIOWrapper
from typing import Callable, Iterator, Optional
from .utils import copy_no_overwrite
from edpu.string_utils import strip_crlf
from os import makedirs
from os.path import exists, dirname


def read_in_chunks(file_object: BufferedReader, size: Optional[int]=None, chunk_size: int=1024*1024) -> Iterator[bytes]:
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M."""

    processed = 0

    while True:
        read_size = chunk_size

        if size is not None:
            read_size = min(read_size, size - processed)

        if read_size <= 0:
            break

        data = file_object.read(read_size)

        if not data:
            break

        processed += len(data)

        yield data


def copy_in_chunks(in_: BufferedReader, out_: BufferedWriter, size: Optional[int]=None, chunk_size: int=1024*1024) -> int:
    processed = 0

    for in_chunk in read_in_chunks(in_, size, chunk_size):
        out_.write(in_chunk)
        processed += len(in_chunk)

    return processed


def parse_ref_line(line: str) -> tuple[str, str]:
    si = line.find(' ')

    if si == -1:
        raise Exception('parse_ref_line')

    return (line[:si], line[si+1:])


class Packer:
    def __init__(self: Packer, in_data: list[tuple[str, str]], out_ref_path: str, out_bin_path: str) -> None:
        self._in_data = in_data
        self._out_ref_path = out_ref_path
        self._out_bin_path = out_bin_path

    def run(self: Packer) -> None:
        with open(self._out_ref_path, 'w') as out_ref:
            with open(self._out_bin_path, 'wb') as out_bin:
                self._copy(out_ref, out_bin)

    def _copy(self: Packer, out_ref: TextIOWrapper, out_bin: BufferedWriter) -> None:
        for in_data_key, in_data_path in self._in_data:
            with open(in_data_path, 'rb') as in_data_file:
                print('Packing ' + in_data_path)
                copy_size = copy_in_chunks(in_data_file, out_bin)
                out_ref.write(str(copy_size) + ' ' + in_data_key + '\n')


class Unpacker:
    def __init__(self: Unpacker, in_data: list[tuple[str, str]], name_provider: Callable[[str], list[str]], unused_hashes_path: str) -> None:
        self._in_data = in_data
        self._name_provider = name_provider
        self._unused_hashes_path = unused_hashes_path

    def run(self: Unpacker) -> None:
        with open(self._unused_hashes_path, 'w') as unused_hashes:
            self._unused_hashes = unused_hashes
            self._unpack_all()

    def _unpack_all(self: Unpacker) -> None:
        for ref_path, bin_path in self._in_data:
            with open(ref_path) as ref:
                with open(bin_path, 'rb') as bin:
                    self._unpack(ref, bin)

    def _unpack(self: Unpacker, ref: TextIOWrapper, bin: BufferedReader) -> None:
        for ref_line in ref.readlines():
            ref_line = strip_crlf(ref_line)
            ref_line = parse_ref_line(ref_line)

            out_size = int(ref_line[0])
            out_key = ref_line[1]
            out_names = self._name_provider(out_key)

            if len(out_names) == 0:
                self._unused_hashes.write(out_key + '\n')
                bin.seek(out_size, 1)
                continue

            out_name = out_names[0]

            if exists(out_name):
                raise Exception('exists(out_name)')

            print('Unpacking ' + out_name)

            makedirs(dirname(out_name), exist_ok=True)

            with open(out_name, 'wb') as out:
                if copy_in_chunks(bin, out, out_size) != out_size:
                    raise Exception('copy_in_chunks(bin, out, out_size) != out_size')

            for out_name in out_names[1:]:
                print('Copying ' + out_name)
                makedirs(dirname(out_name), exist_ok=True)
                copy_no_overwrite(out_names[0], out_name)
