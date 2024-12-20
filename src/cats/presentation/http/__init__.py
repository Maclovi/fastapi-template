from typing import TYPE_CHECKING

from . import breeds, cats, index

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_routes(app: "FastAPI", /) -> None:
    app.include_router(cats.router)
    app.include_router(breeds.router)
    app.include_router(index.router)
