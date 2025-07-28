from sqlalchemy import Connection, CursorResult, Row
from typing import Any, Iterator, Sequence


DISTINCT = 'DISTINCT'
FROM = 'FROM'
IS = 'IS'
JOIN = 'JOIN'
LEFT = 'LEFT'
NOT = 'NOT'
NULL = 'NULL'
ON = 'ON'
OP_EQ = '='
OP_NEQ = '<>'
ORDER_BY = 'ORDER BY'
SELECT = 'SELECT'
WHERE = 'WHERE'


def get_table_column_str(table: str, column: str) -> str:
    from .string_utils import backtick_wrap
    return backtick_wrap(table) + '.' + backtick_wrap(column)


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


def execute_sql_for_one_column_of_all(connection: Connection, sql: str) -> Iterator[str]:
    return get_one_column(execute_sql(connection, sql).all())


def get_distinct_values(connection: Connection, table: str, column: str) -> Iterator[str]:
    return execute_sql_for_one_column_of_all(connection, get_distinct_values_sql(table, column))
