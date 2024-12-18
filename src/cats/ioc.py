from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
)
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.repositories import BreedRepository, CatRepository
from cats.application.common.committer import Transaction
from cats.config import APIConfig, PostgresConfig, load_config
from cats.domain.protocols import (
    BreedRepositoryProtocol,
    CatRepositoryProtocol,
)
from cats.domain.services import BreedService, CatService
from cats.infrastructure.persistence.db_provider import (
    get_engine,
    get_session,
    get_sessionmaker,
)


def config_provider() -> Provider:
    config = load_config()
    proviver = Provider()
    proviver.provide(
        lambda: config.db, scope=Scope.APP, provides=PostgresConfig
    )
    proviver.provide(lambda: config.api, scope=Scope.APP, provides=APIConfig)
    return proviver


def db_provider() -> Provider:
    provider = Provider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(
        get_session,
        scope=Scope.REQUEST,
        provides=AnyOf[Transaction, AsyncSession],
    )
    return provider


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


def setup_providers() -> tuple[Provider, ...]:
    return (
        db_provider(),
        repository_provider(),
        service_provider(),
    )


def init_async_container() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
