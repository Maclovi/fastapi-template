from logging import getLogger

from fastapi import FastAPI

from cats.api import breeds, cats, index
from cats.di import init_dependencies

logger = getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(cats.router)
    app.include_router(breeds.router)
    app.include_router(index.router)
    init_dependencies(app)
    logger.info("App created")

    return app
