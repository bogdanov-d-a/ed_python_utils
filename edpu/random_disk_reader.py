def run(drive_name: str, drive_path: str, block_size: int, device_size: int, sleep_time: float) -> None:
    with open(drive_path, 'rb') as drive_file:
        block_count = device_size // block_size

        while True:
            from binascii import crc32
            from random import randrange
            from time import perf_counter, sleep

            block_number = randrange(block_count)
            print(f'Start reading block ({str(block_size)}) {str(block_number)} of {str(block_count)} from {drive_name} ({drive_path})')

            start_time = perf_counter()

            drive_file.seek(block_number * block_size)
            crc32_ = crc32(drive_file.read(block_size))

            end_time = perf_counter()

            print(f'Success, crc32 is {hex(crc32_)}, read time is {str(end_time - start_time)}, sleep time is {str(sleep_time)}')
            sleep(sleep_time)
