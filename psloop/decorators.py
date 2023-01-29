"""Decorators."""

import functools
from typing import Callable, Optional, Union

from psloop.psloop import Event
from psloop._typing import Interval


def decorator(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def event(func: Union[Callable, Event]):
    @functools.wraps(func)
    def wrapper(
        *args,
        interval: Optional[Interval] = 1,
        **kwargs
    ):
        if isinstance(func, Event):
            pass
        else:
            Event()
    return wrapper
