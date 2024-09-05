from _typeshed import Incomplete
from amsdal_data.connections.manager import ConnectionsManager as ConnectionsManager
from amsdal_data.transactions.background.connections.base import WorkerConnectionBase as WorkerConnectionBase
from amsdal_utils.utils.singleton import Singleton
from collections.abc import Callable as Callable
from typing import Any

class BackgroundTransactionManager(metaclass=Singleton):
    __connection: Incomplete
    __transactions_cache: Incomplete
    def __init__(self) -> None: ...
    def initialize_connection(self, *, raise_on_no_worker: bool = False) -> None:
        """Retrieve connection config from AmsdalConfigManager and initialize connection"""
    def register_connection(self, connection: WorkerConnectionBase) -> None: ...
    def register_transaction(self, func: Callable[..., Any], **transaction_kwargs: Any) -> None: ...
    @property
    def connection(self) -> WorkerConnectionBase: ...
