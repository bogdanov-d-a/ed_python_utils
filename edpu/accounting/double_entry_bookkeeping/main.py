from .file_loggers import *
from .account_manager import *


def run(callback):
    fl = FileLoggers()
    am = AccountManager(fl.make_logger)
    callback(am)
