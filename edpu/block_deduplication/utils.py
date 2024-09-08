HASH_SIZE = 32


def hash(data: bytes) -> bytes:
    from hashlib import sha256

    result = sha256(data).digest()

    if len(result) != HASH_SIZE:
        raise Exception('len(result) != HASH_SIZE')

    return result


def get_hash_path(hash: bytes) -> tuple[str, str]:
    hex = hash.hex()
    return (hex[:2], hex[2:])


def create_blob_file(path: str, data: bytes) -> None:
    with open(path, 'wb') as file:
        file.write(data)


def read_blob_file(path: str, block_size: int) -> bytes:
    from ..disk_utils.utils.io import open_file_rb

    with open_file_rb(path) as file:
        data = file.read()

        if len(data) != block_size:
            raise Exception('len(data) != block_size')

        return data
