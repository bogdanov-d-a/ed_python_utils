from __future__ import annotations
from .context_manager import DummyContextManager
from typing import Any, Callable


class TimeBased:
    def __init__(self: TimeBased, period: float) -> None:
        self._period = period
        self._last = None

    def need_alert(self: TimeBased) -> bool:
        from time import time

        now = time()

        if self._last is None:
            self._last = now
            return False

        if now - self._last > self._period:
            self._last = now
            return True

        return False


class TimeBasedAggregator:
    def __init__(self: TimeBasedAggregator, period: float, start_value: Any, aggregate: Callable[[Any, Any], Any]) -> None:
        self._tb = TimeBased(period)
        self._value = start_value
        self._aggregate = aggregate

    def need_alert(self: TimeBasedAggregator, value: Any) -> bool:
        self._value = self._aggregate(self._value, value)
        return self._tb.need_alert()

    def get_value(self: TimeBasedAggregator) -> Any:
        return self._value

    def get_printer(self: TimeBasedAggregator, annotation: str, print_lock: Any=DummyContextManager()) -> Callable[[Any], None]:
        def fn(value: Any) -> None:
            if self.need_alert(value):
                with print_lock:
                    print(f'{annotation} - {self.get_value()}')

        return fn

    @staticmethod
    def make_number_sum(period: float, start_value: Any=0) -> TimeBasedAggregator:
        return TimeBasedAggregator(period, start_value, lambda a, b: a + b)

    @staticmethod
    def wrap_fn_for_count(fn: Callable[[Any], None]) -> Callable[[], None]:
        return lambda: fn(1)

    @staticmethod
    def make_number_sum_printer(period: float, annotation: str, start_value: Any=0, print_lock: Any=DummyContextManager()) -> Callable[[Any], None]:
        return TimeBasedAggregator.make_number_sum(period, start_value).get_printer(annotation, print_lock)

    @staticmethod
    def make_count_printer(period: float, annotation: str, print_lock: Any=DummyContextManager()) -> Callable[[], None]:
        return TimeBasedAggregator.wrap_fn_for_count(TimeBasedAggregator.make_number_sum_printer(period, annotation, print_lock=print_lock))
