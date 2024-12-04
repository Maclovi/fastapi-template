import os
from collections.abc import AsyncIterator
from typing import cast

import pytest
from dishka import AsyncContainer
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from cats.adapters.database.models import metadata
from cats.web import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    os.environ["POSTGRES_URI"] = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
    )
    os.environ["SQLALCHEMY_DEBUG"] = "true"
    app = create_app()
    return app


@pytest.fixture(scope="session")
def container(app: FastAPI) -> AsyncContainer:
    return cast(AsyncContainer, app.state.dishka_container)


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def engine(container: AsyncContainer) -> AsyncEngine:
    return cast(AsyncEngine, await container.get(AsyncEngine))


@pytest.fixture
async def session(container: AsyncContainer) -> AsyncIterator[AsyncSession]:
    async with container() as c_request:
        yield await c_request.get(AsyncSession)


@pytest.fixture(scope="session", autouse=True)
async def create_tables(engine: AsyncEngine) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield None
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
