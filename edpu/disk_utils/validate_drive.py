from .utils.drive_block_data import DriveBlockData
from typing import Optional


def validate_drive_random(drive_block: DriveBlockData, max_cached_blocks: int, crc_path: Optional[str], echo_rate: int) -> None:
    from .utils.io import open_drive

    with open_drive(drive_block.drive.path) as drive_file:
        from .utils.crc import load_crc_file
        from .utils.utils import get_block_count
        from queue import Queue
        from threading import Thread
        from time import perf_counter

        block_count = get_block_count(drive_block.drive.size, drive_block.size)
        crc_data = load_crc_file(crc_path) if crc_path is not None else None
        blocks_read = 0

        validate_crc_tasks: Queue[tuple[bytes, int]] = Queue(max_cached_blocks)

        def validate_crc_worker() -> None:
            while True:
                from .utils.crc import validate_crc

                validate_crc_task = validate_crc_tasks.get()

                if crc_data is not None:
                    validate_crc(validate_crc_task[0], validate_crc_task[1], crc_data)

                validate_crc_tasks.task_done()

        Thread(target=validate_crc_worker, daemon=True).start()

        total_start = perf_counter()

        try:
            while True:
                from .utils.io import read_block_helper
                from random import randrange

                block_number = randrange(block_count)
                drive_data = read_block_helper(drive_file, drive_block.size, block_number)
                validate_crc_tasks.put((drive_data, block_number))

                if blocks_read % echo_rate == 0:
                    now = perf_counter()
                    now_duration = now - total_start
                    print('blocks_read - ' + str(blocks_read) + ', block_number - ' + str(block_number) + ', now_duration - ' + str(now_duration))

                blocks_read += 1

        finally:
            validate_crc_tasks.join()

            total_end = perf_counter()
            total_duration = total_end - total_start
            print('total_duration - ' + str(total_duration))


def validate_drive_butterfly(drive_block: DriveBlockData, max_cached_blocks: int, crc_path: Optional[str], echo_rate: int) -> None:
    from .utils.io import open_drive

    with open_drive(drive_block.drive.path) as drive_file:
        from .utils.crc import load_crc_file
        from .utils.utils import get_block_count
        from queue import Queue
        from threading import Thread
        from time import perf_counter

        block_count = get_block_count(drive_block.drive.size, drive_block.size)
        crc_data = load_crc_file(crc_path) if crc_path is not None else None
        passes = 0

        validate_crc_tasks: Queue[tuple[bytes, int]] = Queue(max_cached_blocks)

        def validate_crc_worker() -> None:
            while True:
                from .utils.crc import validate_crc

                validate_crc_task = validate_crc_tasks.get()

                if crc_data is not None:
                    validate_crc(validate_crc_task[0], validate_crc_task[1], crc_data)

                validate_crc_tasks.task_done()

        Thread(target=validate_crc_worker, daemon=True).start()

        total_start = perf_counter()

        try:
            while True:
                blocks_read = 0
                range_start = 0
                range_end = block_count
                range_size = block_count
                range_is_start = False

                while range_size > 0:
                    from .utils.io import read_block_helper

                    block_number = range_start if range_is_start else range_end - 1
                    drive_data = read_block_helper(drive_file, drive_block.size, block_number)
                    validate_crc_tasks.put((drive_data, block_number))

                    if blocks_read % echo_rate < 2:
                        now = perf_counter()
                        now_duration = now - total_start
                        print('blocks_read - ' + str(blocks_read) + ', passes - ' + str(passes) + ', block_number - ' + str(block_number) + ', now_duration - ' + str(now_duration))

                    blocks_read += 1

                    if range_is_start:
                        range_start += 1
                    else:
                        range_end -= 1

                    range_size -= 1
                    range_is_start = not range_is_start

                passes += 1

        finally:
            validate_crc_tasks.join()

            total_end = perf_counter()
            total_duration = total_end - total_start
            print('total_duration - ' + str(total_duration))
