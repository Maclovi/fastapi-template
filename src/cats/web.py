import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from cats.adapters.database.models import map_tables
from cats.api import breeds, cats, index
from cats.ioc import init_async_container

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def _setup_conf_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
    )


def _setup_container(app: FastAPI, /) -> None:
    container = init_async_container()
    setup_dishka(container, app)


def _setup_routers(app: FastAPI, /) -> None:
    app.include_router(cats.router)
    app.include_router(breeds.router)
    app.include_router(index.router)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    _setup_container(app)
    _setup_routers(app)
    _setup_conf_logger()
    map_tables()
    logger.info("App created")
    return app
