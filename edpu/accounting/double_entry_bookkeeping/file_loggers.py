from .logger import *
import codecs
import os


class FileLoggers:
    def __init__(self):
        self._loggers = []

    def __del__(self):
        for logger in self._loggers:
            with codecs.open('reports' + os.path.sep + logger.name + '.txt', 'w', 'utf-8') as report_file:
                report_file.write(logger.data)

    def make_logger(self, name):
        logger = Logger(name)
        self._loggers.append(logger)
        return logger
