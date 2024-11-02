from typing import Optional


def backup(input_path: str, blobs_path: str, map_path: str, tail_path: Optional[str], block_size: int) -> None:
    from ..disk_utils.utils.io import open_file_rb

    with open_file_rb(input_path) as input_file:
        with open(map_path, 'wb') as map_file:
            from ..throttling import TimeBasedAggregator

            def calibrate() -> tuple[int, int]:
                from ..div_mod import div_mod
                from os import SEEK_END

                input_file.seek(0, SEEK_END)
                return div_mod(input_file.tell(), block_size)

            calibrated_blocks, calibrated_tail = calibrate()

            if (tail_path is None) != (calibrated_tail == 0):
                raise Exception('(tail_path is None) != (calibrated_tail == 0)')

            count_printer = TimeBasedAggregator.make_count_printer(0.5, f'backup block count (of {calibrated_blocks})')

            for input_file_block in range(calibrated_blocks):
                count_printer()

                def input_file_block_handler() -> None:
                    from ..disk_utils.utils.io import read_block_helper
                    from .utils import hash, get_hash_path
                    from os import makedirs, sep
                    from os.path import isfile

                    data = read_block_helper(input_file, block_size, input_file_block)
                    hash_ = hash(data)
                    hash_head, hash_tail = get_hash_path(hash_)

                    map_file.write(hash_)

                    blob_dir = f'{blobs_path}{sep}{hash_head}'
                    blob_file = f'{blob_dir}{sep}{hash_tail}'

                    makedirs(blob_dir, exist_ok=True)

                    if not isfile(blob_file):
                        from .utils import create_blob_file
                        create_blob_file(blob_file, data)

                input_file_block_handler()

            if tail_path is not None:
                if calibrated_tail == 0:
                    raise Exception('calibrated_tail == 0')

                with open(tail_path, 'wb') as tail_file:
                    from ..disk_utils.utils.io import read_helper
                    tail_file.write(read_helper(input_file, calibrated_blocks * block_size, calibrated_tail))
