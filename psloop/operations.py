from typing import Any, Optional
from collections.abc import Callable


class Saveable:
    def __init__(
        self,
        *functions: Callable[..., bool],
        initial_value: Optional[Any] = None,
    ):
        self.prev_value = initial_value
        self.functions = functions

    def __call__(self, value: Any, *args, **kwargs) -> bool:
        if self.prev_value is None:
            self.prev_value = value

        if result := any(
            func(value, self.prev_value, *args, **kwargs)
            for func in self.functions
        ):
            self.prev_value = value

        return result


def increased(
    value: float,
    prev_value: float,
    difference: Optional[float],
) -> bool:
    if difference is None:
        return value >= prev_value
    return value >= prev_value + difference


def decreased(
    value: float,
    prev_value: float,
    difference: Optional[float],
) -> bool:
    if difference is None:
        return value <= prev_value
    return value <= prev_value - difference
