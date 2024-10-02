from collections.abc import AsyncIterator
from functools import partial
from logging import getLogger

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from cats.adapters.depends_stub import Stub
from cats.domain.protocols.uow import UoWProtocol

logger = getLogger(__name__)


def create_async_sessionmaker(db_uri: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={"connect_timeout": 5},
    )
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
    session_maker = create_async_sessionmaker("")

    app.dependency_overrides[AsyncSession] = partial(
        new_session, session_maker
    )
    app.dependency_overrides[UoWProtocol] = new_uow
