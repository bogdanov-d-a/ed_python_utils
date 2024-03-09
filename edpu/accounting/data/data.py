from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar('T')


class Data(ABC, Generic[T]):
    @abstractmethod
    def zero(cls) -> T:
        pass


    @abstractmethod
    def negate(cls, value: T) -> T:
        pass


    @abstractmethod
    def sum(cls, value1: T, value2: T) -> T:
        pass


    @abstractmethod
    def parse(cls, str_: str) -> T:
        pass


    @abstractmethod
    def to_string(cls, value: T) -> str:
        pass
