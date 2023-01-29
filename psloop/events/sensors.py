"""Sensors events."""

from typing import Optional

import psutil

from psloop.conditions import build_condition
from psloop.decorators import event

from psloop._typing import (
    Condition,
    BooleanCondition,
    NumericCondition,
    TimeCondition,
    Reader,
)


psutil.sensors_temperatures()

psutil.sensors_fans()

@event
def battery_event(
    *,
    condition: Optional[Condition] = None,
    percent: Optional[NumericCondition] = None,
    secsleft: Optional[TimeCondition] = None,
    power_plugged: Optional[BooleanCondition] = None,
) -> Reader:
    _condition = build_condition(
        condition=condition,
        percent=percent,
        secsleft=secsleft,
        power_plugged=power_plugged,
    )

    def _reader():
        info = psutil.sensors_battery()
        status = _condition(**info._asdict())
        return (status, info,)

    return _reader
