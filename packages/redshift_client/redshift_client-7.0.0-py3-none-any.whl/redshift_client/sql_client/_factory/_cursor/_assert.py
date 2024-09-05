from .._primitive import (
    DbPrimitiveFactory,
)
from fa_purity import (
    cast_exception,
    FrozenList,
    Maybe,
    Result,
    ResultE,
)
from redshift_client.sql_client._core.primitive import (
    DbPrimitive,
)
from typing import (
    Callable,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def assert_fetch_one(
    result: Optional[_T],
) -> ResultE[Maybe[FrozenList[DbPrimitive]]]:
    if result is None:
        return Result.success(Maybe.empty())
    if isinstance(result, tuple):
        return DbPrimitiveFactory.to_list_of(
            result, DbPrimitiveFactory.from_any
        ).map(lambda x: Maybe.some(x))
    error = TypeError(f"Unexpected fetch_one result; got {type(result)}")
    return Result.failure(cast_exception(error))


def assert_fetch_list(
    result: _T,
) -> ResultE[FrozenList[FrozenList[DbPrimitive]]]:
    _assert: Callable[
        [_R], ResultE[FrozenList[DbPrimitive]]
    ] = lambda i: DbPrimitiveFactory.to_list_of(i, DbPrimitiveFactory.from_any)
    if isinstance(result, tuple):
        return DbPrimitiveFactory.to_list_of(result, _assert)
    error = TypeError(f"Unexpected fetch_all result; got {type(result)}")
    return Result.failure(cast_exception(error))
