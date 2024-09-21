from .drive_block_data import DriveBlockData
from .generate_drive_crc_config import GenerateDriveCrcConfig
from .generate_drive_delays_config import GenerateDriveDelaysConfig
from io import TextIOWrapper
from typing import Optional


def _header(file: TextIOWrapper, alias: str, device_path: str, device_blocks: str) -> None:
    file.write(f'''from edpu.disk_utils.utils.drive_data import DriveData


def get_drive_data() -> DriveData:
    return DriveData('{alias}', '{device_path}', {device_blocks}*512)


''')


def _main(file: TextIOWrapper, generate_drive_delays: bool, generate_drive_crc: bool, refresh_drive: bool) -> None:
    file.write('''if __name__ == '__main__':\n''')

    if generate_drive_delays:
        file.write('    #generate_drive_delays_()\n')

    if generate_drive_crc:
        file.write('    #generate_drive_crc_()\n')

    if refresh_drive:
        file.write('    #refresh_drive_()\n')


def _drive_block_data(file: TextIOWrapper, drive_block_data_list: list[DriveBlockData]) -> None:
    for drive_block_data in drive_block_data_list:
        start_arg = ''
        end_arg = ''

        if drive_block_data.start is not None:
            start_arg = f', start={drive_block_data.start}'

        if drive_block_data.end is not None:
            end_arg = f', end={drive_block_data.end}'

        file.write(f'''    #dbd = DriveBlockData('{drive_block_data.name}', get_drive_data(), {drive_block_data.size}{start_arg}{end_arg})\n''')


def _generate_drive_delays(file: TextIOWrapper, generate_drive_delays_config: GenerateDriveDelaysConfig) -> None:
    file.write('''def generate_drive_delays_() -> None:
    from edpu.disk_utils.generate_drive_delays import generate_drive_delays
    from edpu.disk_utils.utils.drive_block_data import DriveBlockData

''')

    _drive_block_data(file, generate_drive_delays_config.drive_block_data_list)

    file.write('\n    dbd.print()\n\n')

    for generate_drive_delays_data in generate_drive_delays_config.generate_drive_delays_data_list:
        file.write(f'''    #generate_drive_delays(dbd, {generate_drive_delays_data.echo_rate}, {generate_drive_delays_data.trace_thresold})\n''')

    file.write('\n\n')


def _generate_drive_crc(file: TextIOWrapper, generate_drive_crc_config: GenerateDriveCrcConfig) -> None:
    file.write('''def generate_drive_crc_() -> None:
    from edpu.disk_utils.generate_drive_crc import generate_drive_crc
    from edpu.disk_utils.utils.drive_block_data import DriveBlockData

''')

    _drive_block_data(file, generate_drive_crc_config.drive_block_data_list)

    file.write('\n    dbd.print()\n\n')

    for generate_drive_crc_data in generate_drive_crc_config.generate_drive_crc_data_list:
        file.write(f'''    #generate_drive_crc(dbd, {generate_drive_crc_data.batch_blocks}, {generate_drive_crc_data.max_cached_batches}, {generate_drive_crc_data.echo_rate}, 'crc')\n''')

    file.write('\n\n')


def _refresh_drive(file: TextIOWrapper, refresh_drive_drive_block_data_list: list[DriveBlockData]) -> None:
    file.write('''def refresh_drive_() -> None:
    from edpu.disk_utils.refresh_drive import refresh_drive, refresh_drive_tail
    from edpu.disk_utils.utils.drive_block_data import DriveBlockData

''')

    _drive_block_data(file, refresh_drive_drive_block_data_list)

    file.write('\n    dbd.print()\n\n')

    file.write(f'''    #refresh_drive(dbd)\n''')
    file.write(f'''    #refresh_drive_tail(dbd)\n''')

    file.write('\n\n')


def generate(file_name: str, alias: str, device_path: str, device_blocks: str, generate_drive_delays_config: Optional[GenerateDriveDelaysConfig], generate_drive_crc_config: Optional[GenerateDriveCrcConfig], refresh_drive_drive_block_data_list: Optional[list[DriveBlockData]]) -> None:
    with open(file_name + '.py', 'w', encoding='ascii') as file:
        _header(file, alias, device_path, device_blocks)

        if generate_drive_delays_config is not None:
             _generate_drive_delays(file, generate_drive_delays_config)

        if generate_drive_crc_config is not None:
            _generate_drive_crc(file, generate_drive_crc_config)

        if refresh_drive_drive_block_data_list is not None:
            _refresh_drive(file, refresh_drive_drive_block_data_list)

        _main(file, generate_drive_delays_config is not None, generate_drive_crc_config is not None, refresh_drive_drive_block_data_list is not None)
