from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


async def test_health_engine(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        result = await conn.execute(text("select 1"))
        assert result.scalar() == 1


async def test_health_session(session: AsyncSession) -> None:
    stmt = await session.execute(text("select 1"))
    assert stmt.scalar() == 1
