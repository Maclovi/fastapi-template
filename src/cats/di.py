import os
from collections.abc import AsyncIterator
from functools import partial

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from cats.adapters.depends_stub import Stub
from cats.domain.protocols.uow import UoWProtocol


def create_engine() -> AsyncEngine:
    db_uri = os.getenv("POSTGRES_URI")
    if not db_uri:
        raise ValueError("POSTGRES_URI is not set")
    db_uri = "postgresql+psycopg" + db_uri.replace("postgres", "", 1)

    return create_async_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={"connect_timeout": 5},
    )


def create_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def new_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_maker() as session:
        yield session


def new_uow(
    session: AsyncSession = Depends(Stub(AsyncSession)),
) -> AsyncSession:
    return session


def init_dependencies(app: FastAPI) -> None:
    engine = create_engine()
    session_maker = create_async_sessionmaker(engine)

    app.dependency_overrides[AsyncSession] = partial(
        new_session, session_maker
    )
    app.dependency_overrides[UoWProtocol] = new_uow
