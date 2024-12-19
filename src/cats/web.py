import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from pythonjsonlogger import jsonlogger

from cats.infrastructure.bootstrap.ioc import init_async_container
from cats.infrastructure.persistence.models import map_tables
from cats.presentation.http import setup_routers
from cats.presentation.http.middlewares import setup_middlewares

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI, /) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def setup_logger() -> None:
    format_ = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"
    formatter = jsonlogger.JsonFormatter(format_)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])


def setup_container(app: FastAPI, /) -> None:
    container = init_async_container()
    setup_dishka(container, app)


def create_app() -> FastAPI:
    map_tables()
    setup_logger()
    app = FastAPI(lifespan=lifespan, version="0.1.0")
    setup_routers(app)
    setup_container(app)
    setup_middlewares(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
