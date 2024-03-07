from typing import Any


NAME = 'name'
CALLER = 'caller'
VALUE = 'value'


def get_name_value(name: str, value: Any) -> str:
    from ..string_utils import round_brackets_wrap
    return f'{name} = {round_brackets_wrap(str(value))}'


WrapDataDataElem = tuple[str, Any]
WrapDataData = list[WrapDataDataElem]


def wrap_data(name: str, data: WrapDataData) -> str:
    from ..string_utils import merge_with_space
    from operator import itemgetter

    return merge_with_space(
        [name] + list(map(
            lambda data_elem: get_name_value(data_elem[0], data_elem[1]),
            sorted(data, key=itemgetter(0))
        ))
    )
