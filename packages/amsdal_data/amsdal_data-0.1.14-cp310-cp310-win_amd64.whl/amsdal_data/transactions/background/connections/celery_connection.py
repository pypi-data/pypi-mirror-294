import os
from collections.abc import Callable
from datetime import timedelta
from typing import Any

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_init

from amsdal_data.transactions.background.connections.base import WorkerConnectionBase
from amsdal_data.transactions.background.connections.base import WorkerMode
from amsdal_data.transactions.background.schedule.config import SCHEDULE_TYPE
from amsdal_data.transactions.background.schedule.config import ScheduleConfig
from amsdal_data.transactions.background.schedule.crontab import Crontab


class CeleryConnection(WorkerConnectionBase):
    def __init__(self, app: Celery | None = None) -> None:
        self.app = app if app is not None else Celery()
        self.scheduled_tasks: dict[str, dict[str, Any]] = {}

    def _convert_schedule(self, schedule: SCHEDULE_TYPE) -> Any:
        if not isinstance(schedule, (Crontab, int, float, timedelta)):  # noqa: UP038
            msg = 'schedule must be an instance of Crontab, timedelta, int, or float'
            raise ValueError(msg)

        if isinstance(schedule, Crontab):
            return crontab(
                minute=schedule.minute,
                hour=schedule.hour,
                day_of_week=schedule.day_of_week,
                day_of_month=schedule.day_of_month,
                month_of_year=schedule.month_of_year,
            )

        return schedule

    def register_transaction(self, func: Callable[..., Any], **transaction_kwargs: Any) -> None:
        task_name = transaction_kwargs.get('label') or f'{func.__module__}.{func.__name__}'
        self.app.task(func, name=task_name)

        if transaction_kwargs.get('schedule_config') or transaction_kwargs.get('schedule'):
            task_config = {
                'task': task_name,
            }

            if transaction_kwargs.get('schedule_config'):
                schedule_config = transaction_kwargs['schedule_config']
                if not isinstance(schedule_config, ScheduleConfig):
                    msg = 'schedule_config must be an instance of ScheduleConfig'
                    raise ValueError(msg)

                task_config['schedule'] = self._convert_schedule(schedule_config.schedule)

                if schedule_config.args:
                    task_config['args'] = schedule_config.args
                if schedule_config.kwargs:
                    task_config['kwargs'] = schedule_config.kwargs

            if transaction_kwargs.get('schedule'):
                task_config['schedule'] = self._convert_schedule(transaction_kwargs['schedule'])

            self.scheduled_tasks[task_name] = task_config
            self.app.conf.beat_schedule = self.scheduled_tasks

    def submit(
        self,
        func: Callable[..., Any],
        func_args: tuple[Any, ...],
        func_kwargs: dict[str, Any],
        transaction_kwargs: dict[str, Any],
    ) -> None:
        task_name = transaction_kwargs.get('label') or f'{func.__module__}.{func.__name__}'
        task = self.app.tasks[task_name]
        task.apply_async(func_args, func_kwargs)

    def run_worker(
        self,
        init_function: Callable[..., None] | None = None,
        mode: WorkerMode = WorkerMode.EXECUTOR,
    ) -> None:
        if init_function:
            worker_init.connect(init_function)

        if mode == WorkerMode.SCHEDULER:
            self.app.worker_main(argv=['beat'])

        elif mode == WorkerMode.HYBRID:
            self.app.worker_main(argv=['worker', '--beat', '--loglevel=INFO'])

        else:
            self.app.worker_main(argv=['worker', '--loglevel=INFO'])

    def _populate_default_env_vars(self, connection_kwargs: dict[str, Any]) -> dict[str, Any]:
        for parameter_name, env_name in [
            ('broker_url', 'CELERY_BACKEND_URL'),
        ]:
            connection_kwargs.setdefault(parameter_name, os.getenv(env_name))

        return connection_kwargs

    def connect(self, **kwargs: Any) -> None:
        self.app.conf.update(**self._populate_default_env_vars(kwargs))

    def disconnect(self) -> None:
        pass

    @property
    def is_connected(self) -> bool:
        return True

    @property
    def is_alive(self) -> bool:
        return True
