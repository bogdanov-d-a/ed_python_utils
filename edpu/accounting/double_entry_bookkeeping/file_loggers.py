from __future__ import annotations
from .logger import Logger


class FileLoggers:
    def __init__(self: FileLoggers) -> None:
        self._loggers: list[Logger] = []


    def __del__(self: FileLoggers) -> None:
        for logger in self._loggers:
            from codecs import open
            from os.path import sep

            with open('reports' + sep + logger.name + '.txt', 'w', 'utf-8') as report_file:
                report_file.write(logger.data)


    def make_logger(self: FileLoggers, name: str) -> Logger:
        logger = Logger(name)
        self._loggers.append(logger)
        return logger
