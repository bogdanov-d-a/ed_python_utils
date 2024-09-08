def backup(input_path: str, blobs_path: str, map_path: str, block_size: int) -> None:
    from ..disk_utils.utils.io import open_file_rb

    with open_file_rb(input_path) as input_file:
        with open(map_path, 'wb') as map_file:
            def calibrate() -> int:
                from os import SEEK_END

                input_file.seek(0, SEEK_END)
                size = input_file.tell()

                if size % block_size != 0:
                    raise Exception(r'size % block_size != 0')

                return size // block_size

            for input_file_block in range(calibrate()):
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
