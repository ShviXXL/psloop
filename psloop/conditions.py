"""Conditions."""

import re
import operator

from typing import Union, Optional

from psloop.utils import create_coroutine
from psloop.operations import Saveable, increased, decreased
from psloop._typing import (
    Condition,
    OptionalCondition,
    AnyCondition,
)


DIGIT_REGEX  = r'(?:[0-9]+(?:[.][0-9]*)?|[.][0-9]+)'

COMPARISON_REGEX = r'([><]=?)({})'.format(DIGIT_REGEX)
CHANGE_REGEX     = r'(\+-?|-\+?)({})?'.format(DIGIT_REGEX)
EQUALITY_REGEX   = r'(==?|!=)?(.*)'


OPERATIONS = {
    '<': operator.lt,
    '<=': operator.le,
    '': operator.eq,
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '+-': (Saveable, [increased, decreased]),
    '-+': (Saveable, [increased, decreased]),
    '+': (Saveable, [increased]),
    '-': (Saveable, [decreased]),
}


def _parse_value(value: str) -> Union[str, float]:
    try:
        result = float(value)
    except ValueError:
        if value == '':
            result = None
        else:
            result = value

    return result


def parse_condition(condition: str) -> Condition:
    parsed = re.match(r'^{}$'.format(COMPARISON_REGEX), condition) or \
             re.match(r'^{}$'.format(CHANGE_REGEX), condition) or \
             re.match(r'^{}$'.format(EQUALITY_REGEX), condition)

    parsed_operator, parsed_value = parsed.groups()

    operation = OPERATIONS[parsed_operator]
    value = _parse_value(parsed_value)

    if isinstance(operation, tuple):
        func, args = operation
        operation = func(*args)

    return lambda arg: operation(arg, value)


def _build_condition(condition: AnyCondition) -> Condition:
    if callable(condition):
        builded_condition = condition
    elif isinstance(condition, str):
        builded_condition = parse_condition(condition)
    else:
        builded_condition = lambda arg: arg == condition

    return create_coroutine(builded_condition)


def build_condition(
    condition: Optional[OptionalCondition] = None,
    **conditions: AnyCondition
) -> Condition:
    """Build condition."""

    builded_conditions = []
    for arg, value in conditions.items():
        if value is not None:
            func = _build_condition(value)
            builded_conditions.append((arg, func))

    async def check_conditions(**kwargs):
        result = True
        for arg, func in builded_conditions:
            result = result and await func(kwargs.get(arg))
        return result

    if callable(condition):
        builded_condition = create_coroutine(condition)
        async def _condition(**kwargs) -> bool:
            return await builded_condition(**kwargs) and \
                   await check_conditions(**kwargs)

    else:
        async def _condition(**kwargs) -> bool:
            return await check_conditions(**kwargs)

    return _condition
