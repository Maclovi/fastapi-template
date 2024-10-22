import os
from collections.abc import AsyncIterator, Iterator
from typing import cast

import pytest
from dishka import AsyncContainer
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from cats.adapters.database.models import metadata
from cats.web import create_app


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    os.environ["POSTGRES_URI"] = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
    )
    app = create_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def container(client: TestClient) -> AsyncContainer:
    return cast(AsyncContainer, client.app.state.dishka_container)  # type: ignore


@pytest.fixture(scope="session")
async def engine(container: AsyncContainer) -> AsyncEngine:
    return await container.get(AsyncEngine)


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
