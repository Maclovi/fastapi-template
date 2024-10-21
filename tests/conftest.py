import os
from collections.abc import AsyncIterator
from typing import cast

import pytest
from dishka import AsyncContainer
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from cats.adapters.database.models import mapper_registry
from cats.web import create_app


@pytest.fixture(scope="session")
def client() -> TestClient:
    os.environ["POSTGRES_URI"] = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
    )
    app = create_app()
    return TestClient(app)


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


@pytest.fixture(scope="module", autouse=True)
async def create_all_tables(engine: AsyncEngine) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    yield None
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
