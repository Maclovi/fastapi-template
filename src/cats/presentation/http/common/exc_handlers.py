from functools import partial as part
from typing import TYPE_CHECKING, cast

from starlette import status as code
from starlette.requests import Request
from starlette.responses import JSONResponse

from cats.application.common.errors.base import EntityNotFoundError
from cats.entities.common.errors import EntityError, FieldError

if TYPE_CHECKING:
    from fastapi import FastAPI


class StubError(Exception):
    message: str


async def _validate(_: Request, exc: Exception, status: int) -> JSONResponse:
    exc = cast(StubError, exc)
    return JSONResponse(content={"detail": exc.message}, status_code=status)


def setup_exc_handlers(app: "FastAPI") -> None:
    app.add_exception_handler(
        EntityError,
        part(_validate, status=code.HTTP_500_INTERNAL_SERVER_ERROR),
    )
    app.add_exception_handler(
        FieldError,
        part(_validate, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        EntityNotFoundError,
        part(_validate, status=code.HTTP_404_NOT_FOUND),
    )
