from typing import TYPE_CHECKING

from starlette.middleware.cors import CORSMiddleware

from .logger import LoggerMiddleware

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_middlewares(app: "FastAPI", /) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggerMiddleware)
