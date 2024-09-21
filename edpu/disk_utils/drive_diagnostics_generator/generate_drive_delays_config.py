from __future__ import annotations
from .drive_block_data import DriveBlockData
from .generate_drive_delays_data import GenerateDriveDelaysData


class GenerateDriveDelaysConfig:
    def __init__(self: GenerateDriveDelaysConfig, drive_block_data_list: list[DriveBlockData], generate_drive_delays_data_list: list[GenerateDriveDelaysData]) -> None:
        self.drive_block_data_list = drive_block_data_list
        self.generate_drive_delays_data_list = generate_drive_delays_data_list
