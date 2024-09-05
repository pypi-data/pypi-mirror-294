from collections.abc import Callable
from typing import Any

from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.errors import AmsdalInitiationError
from amsdal_utils.utils.singleton import Singleton

from amsdal_data.connections.manager import ConnectionsManager
from amsdal_data.transactions.background.connections.base import WorkerConnectionBase


class BackgroundTransactionManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.__connection: WorkerConnectionBase | None = None
        self.__transactions_cache: list[tuple[Callable[..., Any], dict[str, Any]]] = []

    def initialize_connection(self, *, raise_on_no_worker: bool = False) -> None:
        """Retrieve connection config from AmsdalConfigManager and initialize connection"""
        if self.__connection is not None:
            msg = 'Background transaction connection is already registered'
            raise AmsdalInitiationError(msg)

        _config = AmsdalConfigManager().get_config()

        if not _config.resources_config.worker:
            if raise_on_no_worker:
                msg = 'Worker config is not provided'
                raise AmsdalInitiationError(msg)

            return

        connection_name = _config.resources_config.worker
        connection = ConnectionsManager([]).get_worker_connection(connection_name)

        self.register_connection(connection)

    def register_connection(self, connection: WorkerConnectionBase) -> None:
        self.__connection = connection

        if self.__transactions_cache:
            for func, transaction_kwargs in self.__transactions_cache:
                self.__connection.register_transaction(func, **transaction_kwargs)

            self.__transactions_cache.clear()

    def register_transaction(self, func: Callable[..., Any], **transaction_kwargs: Any) -> None:
        if self.__connection is None:
            self.__transactions_cache.append((func, transaction_kwargs))

        else:
            self.__connection.register_transaction(func, **transaction_kwargs)

    @property
    def connection(self) -> WorkerConnectionBase:
        if self.__connection is None:
            msg = 'Background transaction connection is not registered'
            raise AmsdalInitiationError(msg)
        return self.__connection
