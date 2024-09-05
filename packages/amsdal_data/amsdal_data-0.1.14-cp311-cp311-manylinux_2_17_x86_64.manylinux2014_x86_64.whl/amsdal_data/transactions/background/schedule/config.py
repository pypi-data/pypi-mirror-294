from datetime import timedelta
from typing import Any
from typing import TypeAlias

from amsdal_data.transactions.background.schedule.crontab import Crontab

SCHEDULE_TYPE: TypeAlias = float | int | Crontab | timedelta


class ScheduleConfig:
    def __init__(
        self,
        schedule: SCHEDULE_TYPE,
        args: tuple[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> None:
        self.schedule = schedule
        self.args = args
        self.kwargs = kwargs
