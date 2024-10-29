from io import BufferedReader
from typing import Optional


def _calibrate(map_file: BufferedReader) -> int:
    from .utils import HASH_SIZE
    from os import SEEK_END

    map_file.seek(0, SEEK_END)
    size = map_file.tell()

    if size % HASH_SIZE != 0:
        raise Exception(r'size % HASH_SIZE != 0')

    return size // HASH_SIZE


def fsck(blobs_path: str, map_paths: list[str], block_size: int, move_blobs_path: Optional[str]=None) -> None:
    try:
        from ..disk_utils.utils.io import open_file_rb

        map_files = list(map(
            open_file_rb,
            map_paths
        ))

        calibrated_list = list(map(
            _calibrate,
            map_files
        ))

        def find_reachable_blocks() -> set[bytes]:
            result: set[bytes] = set()

            for map_path, map_file, calibrated in zip(map_paths, map_files, calibrated_list):
                print(f'find_reachable_blocks map_path - {map_path}')

                for map_file_block in range(calibrated):
                    from ..disk_utils.utils.io import read_block_helper
                    from .utils import HASH_SIZE

                    result.add(read_block_helper(map_file, HASH_SIZE, map_file_block))

            return result

        reachable_blocks = find_reachable_blocks()
        print(f'Found {len(reachable_blocks)} reachable blocks')

        def check_reachable_blocks() -> None:
            from ..throttling import TimeBasedAggregator

            count_printer = TimeBasedAggregator.make_count_printer(0.5, f'check_reachable_blocks block count (of {len(reachable_blocks)})')

            for reachable_block in reachable_blocks:
                from .utils import get_hash_path, read_blob_file, hash
                from os import sep

                count_printer()

                hash_head, hash_tail = get_hash_path(reachable_block)
                data = read_blob_file(f'{blobs_path}{sep}{hash_head}{sep}{hash_tail}', block_size)

                if reachable_block != hash(data):
                    raise Exception('reachable_block != hash(data)')

        if move_blobs_path is None:
            check_reachable_blocks()

        def move_blobs() -> None:
            if move_blobs_path is None:
                return

            from ..throttling import TimeBasedAggregator

            count_printer = TimeBasedAggregator.make_count_printer(0.5, f'move_blobs block count (of {len(reachable_blocks)})')

            for reachable_block in reachable_blocks:
                from .utils import get_hash_path
                from os import makedirs, sep, rename

                count_printer()

                hash_head, hash_tail = get_hash_path(reachable_block)

                move_blob_dir = f'{move_blobs_path}{sep}{hash_head}'
                move_blob_file = f'{move_blob_dir}{sep}{hash_tail}'

                makedirs(move_blob_dir, exist_ok=True)
                rename(f'{blobs_path}{sep}{hash_head}{sep}{hash_tail}', move_blob_file)

        move_blobs()

    finally:
        for map_file in map_files:
            map_file.close()
