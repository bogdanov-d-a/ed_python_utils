from typing import Any


def hash_file(file_name: str, hasher: Any) -> str:
    with open(file_name, 'rb') as file:
        from .read_in_chunks import read_in_chunks

        for chunk in read_in_chunks(file):
            hasher.update(chunk)

    return hasher.hexdigest()


def sha1_file(file_name: str) -> str:
    from hashlib import sha1
    return hash_file(file_name, sha1())


def sha512_file(file_name: str) -> str:
    from hashlib import sha512
    return hash_file(file_name, sha512())
