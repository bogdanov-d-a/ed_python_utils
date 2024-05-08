from .utils.drive_block_data import DriveBlockData


def refresh_drive(drive_block: DriveBlockData, stop_file_name: str='refresh_drive', echo_rate: int=1) -> None:
    from .utils.io import open_drive_rw

    with open_drive_rw(drive_block.drive.path) as drive_file:
        from ..stop_file_strategy import StopFileStrategy

        def refresh_blocks(total_start: float, sfs: StopFileStrategy) -> None:
            for refresh_block in range(drive_block.start, drive_block.end + 1):
                def refresh_block_() -> None:
                    from .utils.io import read_block_helper, write_block_helper
                    data = read_block_helper(drive_file, drive_block.size, refresh_block)
                    write_block_helper(drive_file, drive_block.size, refresh_block, data)

                refresh_block_()

                if refresh_block % echo_rate == 0:
                    def print_progress() -> None:
                        from time import perf_counter

                        complete = refresh_block - drive_block.start + 1
                        remaining = drive_block.end - refresh_block

                        now = perf_counter()
                        now_duration = now - total_start

                        print(', '.join([
                            'refresh_block - ' + str(refresh_block),
                            'complete - ' + str(complete) + ' (' + str(complete / drive_block.count) + ')',
                            'remaining - ' + str(remaining) + ' (' + str(remaining / drive_block.count) + ')',
                            'now_duration - ' + str(now_duration),
                        ]))

                    print_progress()

                    if sfs.need_stop():
                        print('StopFileStrategy stop')
                        return

        def impl() -> None:
            from time import perf_counter

            total_start = perf_counter()

            refresh_blocks(total_start, StopFileStrategy(stop_file_name))

            total_end = perf_counter()
            total_duration = total_end - total_start
            print('total_duration - ' + str(total_duration))

        impl()


def refresh_drive_tail(drive_block: DriveBlockData) -> None:
    from .utils.io import open_drive_rw

    if drive_block.tail <= 0:
        raise Exception('drive_block.tail <= 0')

    with open_drive_rw(drive_block.drive.path) as drive_file:
        from .utils.io import read_helper, write_helper

        offset = drive_block.drive.size - drive_block.tail

        data = read_helper(drive_file, offset, drive_block.tail)
        write_helper(drive_file, offset, data)
