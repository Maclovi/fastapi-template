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

from cats.adapters.database.repositories import BreedRepository, CatRepository
from cats.adapters.depends_stub import Stub
from cats.domain.services import BreedService, CatService


class CatServiceProvider:
    @classmethod
    def cat_provider(
        cls, session: AsyncSession = Depends(Stub(AsyncSession))
    ) -> CatService:
        return CatService(
            CatRepository(session), BreedRepository(session), session
        )


class BreedServiceProvider:
    @classmethod
    def breed_provider(
        cls,
        session: AsyncSession = Depends(Stub(AsyncSession)),
    ) -> BreedService:
        return BreedService(BreedRepository(session), session)


def create_engine() -> AsyncEngine:
    db_uri = os.getenv(
        "POSTGRES_URI",
        "postgresql+psycopg://postgres:postgres@postgres:5432/defaultdb",
    )
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


def cat_provider(
    session: AsyncSession = Depends(Stub(AsyncSession)),
) -> CatService:
    return CatService(
        CatRepository(session), BreedRepository(session), session
    )


def init_dependencies(app: FastAPI) -> None:
    engine = create_engine()
    session_maker = create_async_sessionmaker(engine)

    app.dependency_overrides[AsyncSession] = partial(
        new_session, session_maker
    )
    app.dependency_overrides[CatServiceProvider] = (
        CatServiceProvider.cat_provider
    )
    app.dependency_overrides[BreedServiceProvider] = (
        BreedServiceProvider.breed_provider
    )
