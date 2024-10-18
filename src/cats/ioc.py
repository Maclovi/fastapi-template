import os
from collections.abc import AsyncIterator
from typing import NewType

from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from cats.adapters.database.repositories import BreedRepository, CatRepository
from cats.domain.protocols import (
    BreedRepositoryProtocol,
    CatRepositoryProtocol,
    UoWProtocol,
)
from cats.domain.services import BreedService, CatService

DBURI = NewType("DBURI", str)


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def db_uri(self) -> DBURI:
        db_uri = os.getenv("POSTGRES_URI")
        if db_uri is None:
            raise ValueError("POSTGRES_URI is not set")
        return DBURI(db_uri)

    @provide(scope=Scope.APP)
    async def create_engine(self, db_uri: DBURI) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            db_uri,
            echo=True,
            pool_size=15,
            max_overflow=15,
            connect_args={"connect_timeout": 5},
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def create_async_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine, autoflush=False, expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST)
    async def new_async_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AnyOf[AsyncSession, UoWProtocol]]:
        async with session_factory() as session:
            yield session


def repository_provider() -> Provider:
    provider = Provider()
    provider.provide(
        BreedRepository, scope=Scope.REQUEST, provides=BreedRepositoryProtocol
    )
    provider.provide(
        CatRepository, scope=Scope.REQUEST, provides=CatRepositoryProtocol
    )
    return provider


def service_provider() -> Provider:
    provider = Provider()
    provider.provide(BreedService, scope=Scope.REQUEST)
    provider.provide(CatService, scope=Scope.REQUEST)
    return provider


def init_async_container() -> AsyncContainer:
    providers = [
        DBProvider(),
        repository_provider(),
        service_provider(),
    ]
    return make_async_container(*providers)
