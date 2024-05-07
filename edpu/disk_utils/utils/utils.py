def get_block(data: bytes, block_size: int, skip_blocks: int) -> bytes:
    result = data[block_size * skip_blocks : block_size * (skip_blocks + 1)]

    if len(result) != block_size:
        raise Exception('len(result) != block_size')

    return result


def get_block_count(drive_size: int, block_size: int) -> int:
    if drive_size % block_size != 0:
        raise Exception(r'drive_size % block_size != 0')

    return drive_size // block_size
