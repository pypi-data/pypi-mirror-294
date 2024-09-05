import logging
from collections.abc import Callable
from typing import Any

from amsdal_data.transactions.background.connections.base import WorkerConnectionBase
from amsdal_data.transactions.background.connections.base import WorkerMode

logger = logging.getLogger(__name__)


class SyncBackgroundTransactionConnection(WorkerConnectionBase):
    def __init__(self) -> None:
        pass

    def register_transaction(self, func: Callable[..., Any], **transaction_kwargs: Any) -> None:
        pass

    def submit(
        self,
        func: Callable[..., Any],
        func_args: tuple[Any, ...],
        func_kwargs: dict[str, Any],
        transaction_kwargs: dict[str, Any],  # noqa: ARG002
    ) -> None:
        return func(*func_args, **func_kwargs)

    def run_worker(
        self,
        init_function: Callable[..., None] | None = None,  # noqa: ARG002
        mode: WorkerMode = WorkerMode.EXECUTOR,  # noqa: ARG002
    ) -> None:
        logger.warning('SyncBackgroundTransactionConnection does not support running workers')

    def connect(self, **kwargs: Any) -> None:
        pass

    def disconnect(self) -> None:
        pass

    @property
    def is_connected(self) -> bool:
        return True

    @property
    def is_alive(self) -> bool:
        return True
