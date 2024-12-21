import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from cats.infrastructure.bootstrap.configs import (
    APIConfig,
    PostgresConfig,
    load_configs,
)
from cats.infrastructure.bootstrap.ioc import setup_providers
from cats.infrastructure.bootstrap.log import setup_logger
from cats.infrastructure.persistence.models import map_tables
from cats.presentation.http.common.exc_handlers import setup_exc_handlers
from cats.presentation.http.middlewares import setup_middlewares
from cats.presentation.http.routes import setup_routes

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI, /) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
    configs = load_configs()
    context = {APIConfig: configs.api, PostgresConfig: configs.db}
    container = make_async_container(*setup_providers(), context=context)
    map_tables()
    setup_logger()
    setup_routes(app)
    setup_exc_handlers(app)
    setup_middlewares(app, api_config=configs.api)
    setup_dishka(container, app)
    logger.info("App created", extra={"app_version": app.version})
    return app
