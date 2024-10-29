from __future__ import annotations
from .utils.drive_block_data import DriveBlockData


class _Data:
    def __init__(self: _Data) -> None:
        self.count = 0
        self.delay = 0


    def add(self: _Data, delay: float) -> None:
        self.count += 1
        self.delay += delay


def generate_drive_delays(drive_block: DriveBlockData, echo_rate: int, trace_thresold: float) -> None:
    from .utils.io import open_drive

    with open_drive(drive_block.drive.path) as drive_file:
        from typing import Optional

        stats: dict[int, _Data] = {}

        def add_stat(delay: float) -> None:
            from math import ceil

            delay_ms = ceil(delay*10000)

            if delay_ms > 50:
                delay_ms = ceil(delay*1000)*10

            if delay_ms not in stats:
                stats[delay_ms] = _Data()

            stats[delay_ms].add(delay)

        def print_stats(total_start: float, read_block: Optional[int]) -> None:
            from sys import stdout

            if read_block is not None:
                from time import perf_counter

                complete = read_block - drive_block.start + 1
                remaining = drive_block.end - read_block

                now = perf_counter()
                now_duration = now - total_start

                print(', '.join([
                    'read_block - ' + str(read_block),
                    'complete - ' + str(complete) + ' (' + str(complete / drive_block.count) + ')',
                    'remaining - ' + str(remaining) + ' (' + str(remaining / drive_block.count) + ')',
                    'now_duration - ' + str(now_duration),
                ]))

            print(', '.join(map(
                lambda stats_item: str(stats_item[0]) + ': ' + str((stats_item[1].count, stats_item[1].delay)),
                sorted(stats.items(), key=lambda stats_item: stats_item[0])
            )))

            stdout.flush()

        def read_blocks(total_start: float) -> None:
            for read_block in range(drive_block.start, drive_block.end + 1):
                def read_block_() -> float:
                    from .utils.io import read_block_helper
                    from time import perf_counter

                    start = perf_counter()
                    read_block_helper(drive_file, drive_block.size, read_block)
                    end = perf_counter()

                    return end - start

                duration = read_block_()
                add_stat(duration)

                if duration >= trace_thresold:
                    from sys import stdout
                    print('trace_block ' + str(read_block) + ' ' + str(duration))
                    stdout.flush()

                if read_block % echo_rate == 0:
                    print_stats(total_start, read_block)

        def impl() -> None:
            from time import perf_counter

            total_start = perf_counter()

            read_blocks(total_start)

            total_end = perf_counter()
            total_duration = total_end - total_start

            print_stats(total_start, None)
            print('total_duration - ' + str(total_duration))

        impl()
