from .utils.drive_block_data import DriveBlockData


def generate_drive_crc(drive_block: DriveBlockData, batch_blocks: int, max_cached_batches: int, echo_rate: int, crc_path: str) -> None:
    from .utils.io import open_drive

    with open_drive(drive_block.drive.path) as drive_file:
        with open(crc_path, 'wb') as crc_file:
            from .utils.utils import get_block_count
            from queue import Queue
            from threading import Thread
            from time import perf_counter

            block_count = get_block_count(drive_block.drive.size, drive_block.size)
            batch_count = block_count // batch_blocks
            batch_remain = block_count % batch_blocks
            batch_size = drive_block.size * batch_blocks

            push_crc_to_file_tasks: Queue[tuple[bytes, int]] = Queue(max_cached_batches)

            def push_crc_to_file_worker() -> None:
                while True:
                    from .utils.crc import push_crc_to_file

                    push_crc_to_file_task = push_crc_to_file_tasks.get()
                    push_crc_to_file(push_crc_to_file_task[0], drive_block.size, push_crc_to_file_task[1], crc_file)
                    push_crc_to_file_tasks.task_done()

            Thread(target=push_crc_to_file_worker, daemon=True).start()

            total_start = perf_counter()

            for read_batch in range(batch_count):
                from .utils.io import read_helper
                drive_data = read_helper(drive_file, read_batch * batch_size, batch_size)

                if read_batch % echo_rate == 0:
                    now = perf_counter()
                    now_duration = now - total_start
                    print(f'read_batch - {str(read_batch)} of {str(batch_count)}, now_duration - {str(now_duration)}')

                push_crc_to_file_tasks.put((drive_data, batch_blocks))

            if batch_remain != 0:
                from .utils.io import read_helper
                drive_data = read_helper(drive_file, batch_count * batch_size, drive_block.size * batch_remain)
                push_crc_to_file_tasks.put((drive_data, batch_remain))

            push_crc_to_file_tasks.join()

            total_end = perf_counter()
            total_duration = total_end - total_start
            print('total_duration - ' + str(total_duration))
