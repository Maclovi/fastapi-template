from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from cats.infrastructure.bootstrap.configs import PostgresConfig


async def get_engine(config: PostgresConfig) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        config.uri,
        echo=config.debug,
        pool_size=15,
        max_overflow=15,
        connect_args={"connect_timeout": 5},
    )
    yield engine
    await engine.dispose()


async def get_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, autoflush=False, expire_on_commit=False
    )


async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
