from sqlalchemy import Connection, CursorResult, Row
from typing import Any, Callable, Iterator, Sequence


AND = 'AND'
COUNT = 'COUNT'
DISTINCT = 'DISTINCT'
FROM = 'FROM'
INSERT = 'INSERT'
INTO = 'INTO'
IS = 'IS'
JOIN = 'JOIN'
LEFT = 'LEFT'
NOT = 'NOT'
NULL = 'NULL'
ON = 'ON'
OP_EQ = '='
OP_NEQ = '<>'
OR = 'OR'
ORDER_BY = 'ORDER BY'
SELECT = 'SELECT'
VALUES = 'VALUES'
WHERE = 'WHERE'


def get_table_column_str(table: str, column: str) -> str:
    from .string_utils import backtick_wrap
    return backtick_wrap(table) + '.' + backtick_wrap(column)


def round_brackets_enumeration(list_: list[str], conv: Callable[[str], str]) -> str:
    from .string_utils import round_brackets_wrap, comma_separate

    return round_brackets_wrap(
        comma_separate(
            list(map(conv, list_))
        )
    )


def execute_sql(connection: Connection, sql: str) -> CursorResult[Any]:
    from sqlalchemy.sql import text
    return connection.execute(text(sql))


def get_one_column(sequence: Sequence[Row[Any]]) -> Iterator[Any]:
    return map(
        lambda row: row[0],
        sequence
    )


def get_distinct_values_sql(table: str, column: str) -> str:
    from .string_utils import merge_with_space, backtick_wrap

    return merge_with_space([
        SELECT,
        DISTINCT,
        backtick_wrap(column),
        FROM,
        backtick_wrap(table),
        ORDER_BY,
        backtick_wrap(column),
    ])


def execute_sql_for_one_column_of_one(connection: Connection, sql: str) -> Any:
    return execute_sql(connection, sql).one()[0]


def execute_sql_for_one_column_of_all(connection: Connection, sql: str) -> Iterator[Any]:
    return get_one_column(execute_sql(connection, sql).all())


def get_distinct_values(connection: Connection, table: str, column: str) -> Iterator[Any]:
    return execute_sql_for_one_column_of_all(connection, get_distinct_values_sql(table, column))
