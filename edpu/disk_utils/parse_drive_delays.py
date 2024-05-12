from __future__ import annotations
from typing import Optional


TRACE_BLOCK = 'trace_block'


class TraceBlock:
    def __init__(self: TraceBlock, block: int, delay: float) -> None:
        self.block = block
        self.delay = delay


class StatValue:
    def __init__(self: StatValue, count: int, delay: float) -> None:
        self.count = count
        self.delay = delay


    def add(self: StatValue, other: StatValue) -> None:
        self.count += other.count
        self.delay += other.delay


class ParseDriveDelaysResult:
    def __init__(self: ParseDriveDelaysResult) -> None:
        self.trace_blocks: list[TraceBlock] = []
        self.stats: dict[int, StatValue] = {}


    def add_trace_block(self: ParseDriveDelaysResult, trace_block: TraceBlock) -> None:
        self.trace_blocks.append(trace_block)


    def add_stat(self: ParseDriveDelaysResult, key: int, value: StatValue) -> None:
        if key in self.stats:
            raise Exception()

        self.stats[key] = value


def _parse_trace_block(line: str) -> Optional[TraceBlock]:
    if not line.startswith(TRACE_BLOCK):
        return None

    parts = line.split(' ')

    if len(parts) != 3:
        return None

    if parts[0] != TRACE_BLOCK:
        return None

    try:
        return TraceBlock(int(parts[1]), float(parts[2]))
    except:
        return None


def _parse_stat(delay: str, line: str, result: ParseDriveDelaysResult) -> None:
    parts = line.split(', ')

    if len(parts) != 2:
        raise Exception()

    result.add_stat(int(delay), StatValue(int(parts[0]), float(parts[1])))


def _parse_stats(line: str, result: ParseDriveDelaysResult) -> None:
    index = 0

    while True:
        colon_pos = line.find(': (', index)

        if colon_pos == -1:
            raise Exception()

        delay = line[index : colon_pos]

        close_pos = line.find(')', colon_pos + 3)

        if close_pos == -1:
            raise Exception()

        _parse_stat(delay, line[colon_pos + 3 : close_pos], result)

        if close_pos == len(line) - 1:
            return

        if line[close_pos + 1 : close_pos + 3] != ', ':
            raise Exception()

        index = close_pos + 3


def parse_drive_delays(path: str) -> ParseDriveDelaysResult:
    result = ParseDriveDelaysResult()

    with open(path, encoding='ascii') as file:
        from ..string_utils import strip_crlf

        lines = list(map(
            strip_crlf,
            file.readlines()
        ))

        for line in lines:
            trace_block = _parse_trace_block(line)

            if trace_block is not None:
                result.add_trace_block(trace_block)

        _parse_stats(lines[len(lines) - 2], result)

    return result
