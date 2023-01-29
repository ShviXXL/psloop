from typing import Any
from inspect import iscoroutinefunction
from functools import wraps
from collections.abc import Callable, Awaitable


async def create_coroutine(func: Callable) -> Callable[..., Awaitable[Any]]:
    if iscoroutinefunction(func):
        return func

    @wraps(func)
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
