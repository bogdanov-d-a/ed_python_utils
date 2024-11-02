from __future__ import annotations
from enum import Enum, auto
from io import BufferedWriter
from typing import Optional


class RestoreOutputType(Enum):
    NEW_FILE = auto()
    DRIVE_FILE = auto()


class RestoreOutput:
    def __init__(self: RestoreOutput, type: RestoreOutputType, path: str, minimize_writes: bool=False) -> None:
        self.type = type
        self.path = path
        self.minimize_writes = minimize_writes


    def open(self: RestoreOutput) -> BufferedWriter:
        from ..disk_utils.utils.io import open_drive_rw

        return {
            RestoreOutputType.NEW_FILE: lambda: open(self.path, 'wb'),
            RestoreOutputType.DRIVE_FILE: lambda: open_drive_rw(self.path),
        }[self.type]()


def _swf(file: Optional[BufferedWriter], seek: Optional[int], data: bytes) -> None:
    if file is None:
        raise Exception('file is None')

    if seek is not None:
        file.seek(seek)

    file.write(data)
    file.flush()


def restore(blobs_path: str, map_path: str, tail_path: Optional[str], block_size: int, output: Optional[RestoreOutput]) -> None:
    from ..context_manager import DummyContextManager
    from ..disk_utils.utils.io import open_file_rb

    with open_file_rb(map_path) as map_file:
        with (output.open() if output is not None else DummyContextManager()) as output_file:
            from ..throttling import TimeBasedAggregator
            from .utils import HASH_SIZE

            def calibrate() -> int:
                from ..div_mod import div_mod
                from os import SEEK_END

                map_file.seek(0, SEEK_END)
                result = div_mod(map_file.tell(), HASH_SIZE)

                if result[1] != 0:
                    raise Exception('result[1] != 0')

                return result[0]

            calibrated = calibrate()

            tail_data = None
            tail_size = 0

            if tail_path is not None:
                with open_file_rb(tail_path) as tail_file:
                    tail_data = tail_file.read()
                    tail_size = len(tail_data)

            def calibrate_output() -> None:
                from os import SEEK_END

                if not (output is not None and output.type == RestoreOutputType.DRIVE_FILE):
                    return

                if output_file is None:
                    raise Exception('output_file is None')

                output_file.seek(0, SEEK_END)
                size = output_file.tell()

                if size != calibrated * block_size + tail_size:
                    raise Exception('size != calibrated * block_size + tail_size')

            calibrate_output()

            restore_count_printer = TimeBasedAggregator.make_count_printer(0.5, f'restore block count (of {calibrated})')
            skipped_writing_count_printer = TimeBasedAggregator.make_count_printer(0.5, f'skipped writing block count')

            for map_file_block in range(calibrated):
                restore_count_printer()

                def map_file_block_handler() -> None:
                    from ..disk_utils.utils.io import read_block_helper
                    from .utils import get_hash_path, read_blob_file, hash
                    from os import sep

                    hash_ = read_block_helper(map_file, HASH_SIZE, map_file_block)
                    hash_head, hash_tail = get_hash_path(hash_)
                    data = read_blob_file(f'{blobs_path}{sep}{hash_head}{sep}{hash_tail}', block_size)

                    if hash_ != hash(data):
                        raise Exception('hash_ != hash(data)')

                    if output is not None:
                        if output.type == RestoreOutputType.DRIVE_FILE:
                            if output.minimize_writes:
                                if output_file is None:
                                    raise Exception('output_file is None')

                                if read_block_helper(output_file, block_size, map_file_block) != data:
                                    _swf(output_file, map_file_block * block_size, data)
                                else:
                                    skipped_writing_count_printer()

                            else:
                                _swf(output_file, map_file_block * block_size, data)

                        elif output.type == RestoreOutputType.NEW_FILE:
                            _swf(output_file, None, data)

                        else:
                            raise Exception()

                map_file_block_handler()

            if tail_path is not None:
                if tail_data is None:
                    raise Exception('tail_data is None')

                if output is not None:
                    if output.type == RestoreOutputType.DRIVE_FILE:
                        if output.minimize_writes:
                            from ..disk_utils.utils.io import read_helper

                            if output_file is None:
                                raise Exception('output_file is None')

                            if read_helper(output_file, calibrated * block_size, tail_size) != tail_data:
                                _swf(output_file, calibrated * block_size, tail_data)
                            else:
                                print('skipped writing tail')

                        else:
                            _swf(output_file, calibrated * block_size, tail_data)

                    elif output.type == RestoreOutputType.NEW_FILE:
                        _swf(output_file, None, tail_data)

                    else:
                        raise Exception()
