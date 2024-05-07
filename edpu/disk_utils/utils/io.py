from io import BufferedRandom, BufferedReader


def open_file_rb(path: str) -> BufferedReader:
    return open(path, 'rb')


def open_drive(drive_path: str) -> BufferedReader:
    return open_file_rb(drive_path)


def open_drive_rw(drive_path: str) -> BufferedRandom:
    return open(drive_path, 'r+b')


def read_helper(file: BufferedReader, offset: int, count: int) -> bytes:
    file.seek(offset)
    data = file.read(count)

    if len(data) != count:
        raise Exception('len(data) != count')

    return data


def read_block_helper(file: BufferedReader, block_size: int, block_number: int) -> bytes:
    return read_helper(file, block_number * block_size, block_size)


def write_helper(file: BufferedRandom, offset: int, data: bytes) -> None:
    file.seek(offset)
    file.write(data)


def write_block_helper(file: BufferedRandom, block_size: int, block_number: int, data: bytes) -> None:
    if len(data) != block_size:
        raise Exception('len(data) != block_size')

    write_helper(file, block_number * block_size, data)
