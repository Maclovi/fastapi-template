import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cats.adapters.database.models import map_tables
from cats.api import breeds, cats, index
from cats.ioc import init_async_container

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def setup_conf_logger() -> None:
    format = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
    logging.basicConfig(level=logging.INFO, format=format, stream=sys.stdout)


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
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    map_tables()
    setup_conf_logger()
    setup_container(app)
    setup_routers(app)
    setup_middlewares(app)
    logger.info("App created")
    return app
