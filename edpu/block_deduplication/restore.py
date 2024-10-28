from typing import Optional


def restore(blobs_path: str, map_path: str, block_size: int, output_path: Optional[str]) -> None:
    from ..context_manager import DummyContextManager
    from ..disk_utils.utils.io import open_file_rb

    with open_file_rb(map_path) as map_file:
        with (open(output_path, 'wb') if output_path is not None else DummyContextManager()) as output_file:
            from ..throttling import TimeBasedAggregator
            from .utils import HASH_SIZE

            def calibrate() -> int:
                from os import SEEK_END

                map_file.seek(0, SEEK_END)
                size = map_file.tell()

                if size % HASH_SIZE != 0:
                    raise Exception(r'size % HASH_SIZE != 0')

                return size // HASH_SIZE

            calibrated = calibrate()
            count_printer = TimeBasedAggregator.make_count_printer(0.5, f'restore block count (of {calibrated})')

            for map_file_block in range(calibrated):
                count_printer()

                def map_file_block_handler() -> None:
                    from ..disk_utils.utils.io import read_block_helper
                    from .utils import get_hash_path, read_blob_file, hash
                    from os import sep

                    hash_ = read_block_helper(map_file, HASH_SIZE, map_file_block)
                    hash_head, hash_tail = get_hash_path(hash_)
                    data = read_blob_file(f'{blobs_path}{sep}{hash_head}{sep}{hash_tail}', block_size)

                    if hash_ != hash(data):
                        raise Exception('hash_ != hash(data)')

                    if output_path is not None:
                        if output_file is None:
                            raise Exception('output_file is None')

                        output_file.write(data)

                map_file_block_handler()
