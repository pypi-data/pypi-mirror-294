from __future__ import (
    annotations,
)

from ._cursor import (
    new_sql_client,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from logging import (
    Logger,
)
import psycopg2 as postgres
from redshift_client.sql_client._core.connection import (
    Credentials,
    DatabaseId,
    DbConnection,
    IsolationLvl,
)
from redshift_client.sql_client._core.cursor import (
    SqlCursor,
)
from typing import (
    Any,
    Callable,
    TYPE_CHECKING,
    TypeVar,
)

if TYPE_CHECKING:
    from psycopg2 import (
        connection as ConnectionStub,
        cursor as CursorStub,
    )
else:
    CursorStub = Any
    ConnectionStub = Any


_T = TypeVar("_T")


@dataclass(frozen=True)
class RedshiftConnection:
    _connection: ConnectionStub

    def _act(self, action: Callable[[ConnectionStub], _T]) -> Cmd[_T]:
        return Cmd.wrap_impure(lambda: action(self._connection))

    @property
    def close(self) -> Cmd[None]:
        return self._act(lambda c: c.close())

    @property
    def commit(self) -> Cmd[None]:
        return self._act(lambda c: c.commit())

    def cursor(self, logger: Logger) -> Cmd[SqlCursor]:
        def _inner(connection: ConnectionStub) -> SqlCursor:
            _cursor: CursorStub = connection.cursor()
            return new_sql_client(logger, _cursor)

        return self._act(_inner)

    @staticmethod
    def connect(
        db_id: DatabaseId,
        creds: Credentials,
        readonly: bool,
        isolation: IsolationLvl,
        autocommit: bool,
    ) -> Cmd[DbConnection]:
        def _action() -> DbConnection:
            connection = postgres.connect(
                dbname=db_id.db_name,
                user=creds.user,
                password=creds.password,
                host=db_id.host,
                port=db_id.port,
            )
            connection.set_session(
                isolation_level=isolation.value,
                readonly=readonly,
                autocommit=autocommit,
            )
            redshift_connection = RedshiftConnection(connection)

            return DbConnection(
                close=redshift_connection.close,
                commit=redshift_connection.commit,
                cursor=redshift_connection.cursor,
            )

        return Cmd.wrap_impure(_action)
