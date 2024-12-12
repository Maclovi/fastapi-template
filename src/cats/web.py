import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pythonjsonlogger import jsonlogger

from cats.adapters.database.models import map_tables
from cats.api import breeds, cats, index
from cats.api.middlewares.logger import LoggerMiddleware
from cats.ioc import init_async_container

logger = logging.getLogger(__name__)


def setup_logger() -> None:
    format_ = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"
    formatter = jsonlogger.JsonFormatter(format_)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])


def setup_container(app: FastAPI, /) -> None:
    container = init_async_container()
    setup_dishka(container, app)


def setup_routers(app: FastAPI, /) -> None:
    app.include_router(cats.router)
    app.include_router(breeds.router)
    app.include_router(index.router)


def setup_middlewares(app: FastAPI, /) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8080",
            "http://127.0.0.1:8080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggerMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI, /) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    map_tables()
    setup_logger()
    app = FastAPI(lifespan=lifespan, version="0.1.0")
    setup_routers(app)
    setup_container(app)
    setup_middlewares(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
