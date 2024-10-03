from __future__ import annotations


class DbLock:
    def __init__(self: DbLock, name: str, timeout: int) -> None:
        from edpu_user.db_lock import get_engine
        from sqlalchemy import create_engine

        self._name = name
        self._timeout = timeout
        self._con = create_engine(get_engine()).connect()

    def __enter__(self: DbLock) -> None:
        from .string_utils import apostrophe_wrap
        from sqlalchemy.sql import text

        if self._con.execute(text(f'SELECT GET_LOCK({apostrophe_wrap(self._name)}, {self._timeout})')).one()[0] != 1:
            raise Exception('GET_LOCK')

    def __exit__(self: DbLock, exc_type, exc_value, exc_tb) -> None:
        from .string_utils import apostrophe_wrap
        from sqlalchemy.sql import text

        if self._con.execute(text(f'SELECT RELEASE_LOCK({apostrophe_wrap(self._name)})')).one()[0] != 1:
            raise Exception('RELEASE_LOCK')

        self._con.close()
