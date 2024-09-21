from __future__ import annotations
from typing import Callable


def get_block_aliases(crc_path: str, get_block_alias: Callable[[bytes, int], str]) -> list[str]:
    from .crc import load_crc_file, get_crc_block_count, get_crc_block

    crc_data = load_crc_file(crc_path)

    return list(map(
        lambda block_index: get_block_alias(get_crc_block(crc_data, block_index), block_index),
        range(get_crc_block_count(crc_data))
    ))


class BlockAliasRange:
    def __init__(self: BlockAliasRange, start: int, count: int, alias: str) -> None:
        self.start = start
        self.end = start + count - 1
        self.count = count
        self.alias = alias

    def tuple_(self: BlockAliasRange) -> tuple[int, int, int, str]:
        return (self.start, self.end, self.count, self.alias)


def get_block_alias_ranges(block_aliases: list[str]) -> list[BlockAliasRange]:
    result: list[BlockAliasRange] = []

    now = None
    now_start = 0
    now_count = 0

    def flush() -> None:
        if now is None:
            raise Exception()

        result.append(BlockAliasRange(now_start, now_count, now))

    for block_alias in block_aliases:
        if now is None:
            now = block_alias
            now_start = 0
            now_count = 1
        else:
            if now == block_alias:
                now_count += 1
            else:
                flush()

                now = block_alias
                now_start += now_count
                now_count = 1

    flush()

    return result


def print_block_alias_ranges(ranges: list[BlockAliasRange]) -> None:
    for tuple_ in list(map(
        lambda range: range.tuple_(),
        ranges
    )):
        print(tuple_)


def print_dd_wipe(ranges: list[BlockAliasRange], dev: str, bs: str) -> None:
    for range in ranges:
        from ...linux.dd_gen import dd_gen_wipe_dev
        print(dd_gen_wipe_dev(dev, bs, str(range.start), str(range.count)))
