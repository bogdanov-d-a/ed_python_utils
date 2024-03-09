from io import BufferedReader
from typing import Any, Iterator


def read_in_chunks(file_object: BufferedReader, chunk_size: int=1024*1024) -> Iterator[bytes]:
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def hash_file(file_name: str, hasher: Any) -> str:
    with open(file_name, 'rb') as file:
        for chunk in read_in_chunks(file):
            hasher.update(chunk)
    return hasher.hexdigest()


def sha1_file(file_name: str) -> str:
    from hashlib import sha1
    return hash_file(file_name, sha1())


def sha512_file(file_name: str) -> str:
    from hashlib import sha512
    return hash_file(file_name, sha512())
