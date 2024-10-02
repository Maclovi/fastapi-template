from collections.abc import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from cats.adapters.database.models import mapper_registry
from cats.di import create_async_sessionmaker, create_engine


@pytest.fixture(scope="module")
def engine() -> AsyncEngine:
    return create_engine()  # type: ignore[no-any-return]


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    session_maker = create_async_sessionmaker(engine)
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="module")
async def create_all_tables(engine: AsyncEngine) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield None

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


async def test_engine(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        result = await conn.execute(text("select 1"))
        assert result.scalar() == 1


async def test_health(session: AsyncSession) -> None:
    stmt = await session.execute(text("select 1"))
    assert stmt.scalar() == 1
