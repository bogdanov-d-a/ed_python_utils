from __future__ import annotations
from typing import Generic, TypeVar, Union


MapperA = TypeVar('MapperA')
MapperB = TypeVar('MapperB')


class Mapper(Generic[MapperA, MapperB]):
    def __init__(self: Mapper[MapperA, MapperB], data: list[tuple[MapperA, MapperB]]) -> None:
        for item in range(2):
            from operator import itemgetter
            Mapper._dup_check(list(map(itemgetter(item), data)))

        self._data = data

    def _dict(self: Mapper[MapperA, MapperB], rev: bool) -> dict[Union[MapperA, MapperB], Union[MapperA, MapperB]]:
        return { b if rev else a: a if rev else b for a, b in self._data }

    def _map(self: Mapper[MapperA, MapperB], u: Union[MapperA, MapperB], rev: bool) -> Union[MapperA, MapperB]:
        return self._dict(rev)[u]

    def fwd(self: Mapper[MapperA, MapperB], a: MapperA) -> MapperB:
        return self._map(a, False) # type: ignore

    def rev(self: Mapper[MapperA, MapperB], b: MapperB) -> MapperA:
        return self._map(b, True) # type: ignore

    @staticmethod
    def _dup_check(data: list) -> None:
        if len(data) != len(set(data)):
            raise Exception(data)
