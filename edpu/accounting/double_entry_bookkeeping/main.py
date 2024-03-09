from ..data.data import Data
from .account_manager import AccountManager
from typing import Callable, TypeVar


T = TypeVar('T')


def run(actions: Data[T], callback: Callable[[AccountManager[T]], None]) -> None:
    from .file_loggers import FileLoggers

    fl = FileLoggers()
    am = AccountManager(actions, fl.make_logger)
    callback(am)
