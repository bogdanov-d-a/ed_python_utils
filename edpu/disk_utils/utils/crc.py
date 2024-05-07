from io import BufferedWriter


def load_crc_file(crc_path: str) -> bytes:
    from .io import open_file_rb

    with open_file_rb(crc_path) as crc_file:
        return crc_file.read()


def get_crc_block(data: bytes, skip_blocks: int) -> bytes:
    from .utils import get_block
    return get_block(data, 20, skip_blocks)


def push_crc_to_file(drive_data: bytes, block_size: int, batch_blocks: int, crc_file: BufferedWriter) -> None:
    for batch_block in range(batch_blocks):
        from .utils import get_block
        from hashlib import sha1

        block = get_block(drive_data, block_size, batch_block)
        crc = sha1(block).digest()
        crc_file.write(crc)


def validate_crc(drive_data: bytes, block_number: int, crc_data: bytes) -> None:
    from hashlib import sha1

    crc_drive = sha1(drive_data).digest()
    crc_match = get_crc_block(crc_data, block_number)

    if crc_drive != crc_match:
        raise Exception('crc_drive != crc_match, block_number - ' + str(block_number))
