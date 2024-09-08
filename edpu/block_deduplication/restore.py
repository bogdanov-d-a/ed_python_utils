def restore(blobs_path: str, map_path: str, block_size: int, output_path: str) -> None:
    from ..disk_utils.utils.io import open_file_rb

    with open_file_rb(map_path) as map_file:
        with open(output_path, 'wb') as output_file:
            from .utils import HASH_SIZE

            def calibrate() -> int:
                from os import SEEK_END

                map_file.seek(0, SEEK_END)
                size = map_file.tell()

                if size % HASH_SIZE != 0:
                    raise Exception(r'size % HASH_SIZE != 0')

                return size // HASH_SIZE

            for map_file_block in range(calibrate()):
                def map_file_block_handler() -> None:
                    from ..disk_utils.utils.io import read_block_helper
                    from .utils import get_hash_path, read_blob_file, hash
                    from os import sep

                    hash_ = read_block_helper(map_file, HASH_SIZE, map_file_block)
                    hash_head, hash_tail = get_hash_path(hash_)
                    data = read_blob_file(f'{blobs_path}{sep}{hash_head}{sep}{hash_tail}', block_size)

                    if hash_ != hash(data):
                        raise Exception('hash_ != hash(data)')

                    output_file.write(data)

                map_file_block_handler()
