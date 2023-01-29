from typing import Union, Any
from collections.abc import Callable, Awaitable
from datetime import timedelta

import psutil


PSUtilCPU = Union[
    psutil.cpu_times,
    psutil.cpu_percent,
    psutil.cpu_times_percent,
    psutil.cpu_count,
    psutil.cpu_stats,
    psutil.cpu_freq,
    psutil.getloadavg,
]
PSUtilMemory = Union[
    psutil.virtual_memory,
    psutil.swap_memory,
]
PSUtilDisks = Union[
    psutil.disk_partitions,
    psutil.disk_usage,
    psutil.disk_io_counters,
]
PSUtilNetwork = Union[
    psutil.net_io_counters,
    psutil.net_connections,
    psutil.net_if_addrs,
    psutil.net_if_stats,
]
PSUtilSensors = Union[
    psutil.sensors_temperatures,
    psutil.sensors_fans,
    psutil.sensors_battery,
]
PSUtilOther = Union[
    psutil.boot_time,
    psutil.users,
]
PSUtilAll = Union[
    PSUtilCPU,
    PSUtilMemory,
    PSUtilDisks,
    PSUtilNetwork,
    PSUtilSensors,
    PSUtilOther
]

Interval = Union[int, float, timedelta]

Condition = Callable[..., Awaitable[bool]]
OptionalCondition = Union[Condition, Callable[..., bool], None]
ParsableCondition = Union[OptionalCondition, str]
BooleanCondition = Union[ParsableCondition, bool]
NumericCondition = Union[ParsableCondition, float]
TimeCondition = Union[NumericCondition, timedelta]

AnyCondition = Union[
    OptionalCondition,
    ParsableCondition,
    BooleanCondition,
    NumericCondition,
    TimeCondition,
]

Function = Union[Callable[..., Any], Callable[..., Awaitable[Any]]]

Reader = Callable[[], tuple[bool, Any]]
