from __future__ import annotations
from .drive_block_data import DriveBlockData
from .generate_drive_crc_data import GenerateDriveCrcData


class GenerateDriveCrcConfig:
    def __init__(self: GenerateDriveCrcConfig, drive_block_data_list: list[DriveBlockData], generate_drive_crc_data_list: list[GenerateDriveCrcData]) -> None:
        self.drive_block_data_list = drive_block_data_list
        self.generate_drive_crc_data_list = generate_drive_crc_data_list
