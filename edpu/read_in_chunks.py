from typing import BinaryIO, Iterator


def read_in_chunks(file_object: BinaryIO, chunk_size: int=1024*1024) -> Iterator[bytes]:
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
