"""PSLoop."""

import asyncio
from typing import Optional, Union
from collections.abc import Coroutine, Callable
from datetime import timedelta

from psloop._typing import (
    Interval,
    Reader,
)


class Event:
    """Event."""

    def __init__(
        self,
        func: Union[Coroutine, Callable],
        reader: Reader,
        *,
        interval: Optional[Interval] = 1
    ):
        self.func = func
        self.reader = reader

        if isinstance(interval, timedelta):
            self.interval = interval.total_seconds()
        else:
            self.interval = interval

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


