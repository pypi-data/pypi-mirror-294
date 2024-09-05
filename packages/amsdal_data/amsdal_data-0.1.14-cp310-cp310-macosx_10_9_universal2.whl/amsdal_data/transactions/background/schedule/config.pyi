from _typeshed import Incomplete
from amsdal_data.transactions.background.schedule.crontab import Crontab as Crontab
from typing import Any, TypeAlias

SCHEDULE_TYPE: TypeAlias

class ScheduleConfig:
    schedule: Incomplete
    args: Incomplete
    kwargs: Incomplete
    def __init__(self, schedule: SCHEDULE_TYPE, args: tuple[Any] | None = None, kwargs: dict[str, Any] | None = None) -> None: ...
