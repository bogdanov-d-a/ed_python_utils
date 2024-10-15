from __future__ import annotations
from typing import Callable


RedundantizerHasher = Callable[[bytes], bytes]


def redundantizer_hasher_sha256() -> RedundantizerHasher:
    from hashlib import sha256
    return lambda data: sha256(data).digest()


class Redundantizer:
    def __init__(
            self: Redundantizer,
            block_size: int,
            signature: bytes,
            signature_count: int,
            size_length: int=8,
            hash_size: int=32,
            hasher: RedundantizerHasher=redundantizer_hasher_sha256()
    ) -> None:
        self._block_size = block_size

        if len(signature) != block_size:
            raise Exception('len(signature) != block_size')

        self._signature = signature
        self._signature_count = signature_count
        self._size_length = size_length
        self._hash_size = hash_size
        self._hasher = hasher


    def _hash(self: Redundantizer, data: bytes) -> bytes:
        result = self._hasher(data)

        if len(result) != self._hash_size:
            raise Exception('len(result) != self._hash_size')

        return result


    def _size_count(self: Redundantizer) -> int:
        if self._hash_size % self._size_length != 0:
            raise Exception(r'self._hash_size % self._size_length != 0')

        return self._hash_size // self._size_length


    def _description_size(self: Redundantizer) -> int:
        return self._hash_size * 2


    def _description_count(self: Redundantizer) -> int:
        if self._block_size % self._description_size() != 0:
            raise Exception(r'self._block_size % self._description_size() != 0')

        return self._block_size // self._description_size()


    def _redundantize(self: Redundantizer, data: bytes) -> bytes:
        result = self._signature * self._signature_count

        size = len(data)
        size_bytes = size.to_bytes(self._size_length)
        hash_ = self._hash(data)

        for _ in range(self._description_count()):
            result += size_bytes * self._size_count()
            result += hash_

        result += data

        tail_size = size % self._block_size

        if tail_size != 0:
            result += b'\x00' * (self._block_size - tail_size)

        return result


    def redundantize(self: Redundantizer, filename_in: str, count: int, filename_out: str) -> None:
        with open(filename_in, 'rb') as file_in:
            data = file_in.read()

        with open(filename_out, 'wb') as file_out:
            redundantize_one_ = self._redundantize(data)

            for _ in range(count):
                file_out.write(redundantize_one_)
