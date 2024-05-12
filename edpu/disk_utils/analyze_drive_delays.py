from .parse_drive_delays import ParseDriveDelaysResult, StatValue
from typing import Optional


def trace_blocks_by_delay_desc(data: ParseDriveDelaysResult, limit: Optional[int]=None) -> None:
    trace_blocks = sorted(data.trace_blocks, key=lambda trace_block: trace_block.delay, reverse=True)

    if limit is not None:
        trace_blocks = trace_blocks[:limit]

    for trace_block in trace_blocks:
        print(trace_block.delay, trace_block.block)


def gen_points(start: int, count: int) -> list[int]:
    result: list[int] = []
    now = start

    for _ in range(count):
        result.append(now)
        now *= 2

    return result


def stats_partition(data: ParseDriveDelaysResult, points: list[int]) -> dict[Optional[int], StatValue]:
    points.sort()
    result: dict[Optional[int], StatValue] = {}

    def find_point(value: int) -> Optional[int]:
        for point in points:
            if value < point:
                return point

        return None

    for stat_key, stat_value in data.stats.items():
        point = find_point(stat_key)

        if point not in result:
            result[point] = StatValue(0, 0)

        result[point].add(stat_value)

    return result


def stats_partition_print(data: ParseDriveDelaysResult, points: list[int]) -> None:
    stats = stats_partition(data, points)

    for stat_key, stat_value in sorted(stats.items(), key=lambda stat: -1 if stat[0] is None else stat[0]):
        print(f'{stat_key}: ({stat_value.count}, {stat_value.delay})')
