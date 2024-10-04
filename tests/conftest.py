import os
from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from cats.adapters.database.models import mapper_registry
from cats.api import breeds, cats, index
from cats.di import create_async_sessionmaker, create_engine, init_dependencies


@pytest.fixture(scope="session", autouse=True)
def _env() -> None:
    os.environ["POSTGRES_URI"] = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
    )


@pytest.fixture(scope="module")
def engine() -> AsyncEngine:
    return create_engine()  # type: ignore[no-any-return]


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    session_maker = create_async_sessionmaker(engine)
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="module", autouse=True)
async def create_all_tables(engine: AsyncEngine) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield None

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


@pytest.fixture(scope="session")
def client() -> TestClient:
    app = FastAPI()
    app.include_router(index.router)
    app.include_router(cats.router)
    app.include_router(breeds.router)
    init_dependencies(app)

    return TestClient(app)
