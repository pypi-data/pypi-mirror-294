from _typeshed import Incomplete
from collections.abc import Callable as Callable
from enum import Enum
from pydantic import BaseModel
from typing import Any, ClassVar

class IcebergDataTypes(str, Enum):
    BOOLEAN = 'boolean'
    INT = 'int'
    BIGINT = 'bigint'
    LONG = 'long'
    FLOAT = 'float'
    DOUBLE = 'double'
    DATE = 'date'
    TIME = 'time'
    TIMESTAMP = 'timestamp'
    STRING = 'string'
    UUID = 'uuid'
    BINARY = 'binary'
    STRUCT = 'struct'
    LIST = 'list'
    MAP = 'map'

python_to_iceberg_types: Incomplete

class ComplexType(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    _type_value: ClassVar[Callable[[Any, IcebergDataTypes | ComplexType], str]]
    def to_sql(self) -> str: ...
    def _type_value(self, value: IcebergDataTypes | ComplexType) -> str: ...

class StructType(ComplexType):
    to_sql: ClassVar[Callable[..., str]]
    fields: dict[str, IcebergDataTypes | ComplexType]
    def to_sql(self) -> str: ...

class MapType(ComplexType):
    to_sql: ClassVar[Callable[..., str]]
    key_type: IcebergDataTypes
    value_type: IcebergDataTypes | ComplexType
    def to_sql(self) -> str: ...

class ListType(ComplexType):
    to_sql: ClassVar[Callable[..., str]]
    element_type: IcebergDataTypes | ComplexType
    def to_sql(self) -> str: ...

class IcebergTableColumn(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    _to_sql_value: ClassVar[Callable[..., str]]
    cid: int
    name: str
    type: IcebergDataTypes | ComplexType
    notnull: int
    def to_sql(self) -> str: ...
    def _to_sql_value(self, value: Any) -> str: ...
    @property
    def type_sql(self) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...

class IcebergTableColumnsSchema(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    columns: list['IcebergTableColumn']
    def to_sql(self) -> str: ...
