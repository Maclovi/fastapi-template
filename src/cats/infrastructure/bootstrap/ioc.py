from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
)
from sqlalchemy.ext.asyncio import AsyncSession

from cats.application.commands.cat.add_cat import AddCatCommandHandler
from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommandHandler,
)
from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.cat import CatGateway
from cats.application.common.transaction import Transaction
from cats.application.queries.breed.get_breeds import GetBreedsQueryHandler
from cats.application.queries.cat.get_cat_by_id import GetCatWithIDQueryHandler
from cats.application.queries.cat.get_cats import GetCatsQueryHandler
from cats.application.queries.cat.get_cats_by_breed import (
    GetCatsWithBreedQueryHandler,
)
from cats.entities.breed.services import BreedService
from cats.entities.cat.services import CatService
from cats.entities.common.tracker import Tracker
from cats.infrastructure.bootstrap.configs import (
    APIConfig,
    PostgresConfig,
    load_config,
)
from cats.infrastructure.gateways.breed import BreedMapper
from cats.infrastructure.gateways.cat import CatMapper
from cats.infrastructure.persistence.db_provider import (
    get_engine,
    get_session,
    get_sessionmaker,
)
from cats.infrastructure.persistence.tracker import SATracker


def configs_provider() -> Provider:
    config = load_config()
    proviver = Provider(scope=Scope.APP)
    proviver.provide(lambda: config.db, provides=PostgresConfig)
    proviver.provide(lambda: config.api, provides=APIConfig)
    return proviver


def db_provider() -> Provider:
    provider = Provider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(
        get_session,
        provides=AnyOf[Transaction, AsyncSession],
        scope=Scope.REQUEST,
    )
    return provider


def gateways_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(CatMapper, provides=CatGateway)
    provider.provide(BreedMapper, provides=BreedGateway)
    provider.provide(SATracker, provides=Tracker)
    return provider


def services_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide_all(CatService, BreedService)
    return provider


def interactors_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide_all(
        GetBreedsQueryHandler,
        GetCatsQueryHandler,
        GetCatWithIDQueryHandler,
        GetCatsWithBreedQueryHandler,
        AddCatCommandHandler,
        DeleteCatCommandHandler,
        UpdateCatDescriptionCommandHandler,
    )
    return provider


def setup_providers() -> tuple[Provider, ...]:
    return (
        configs_provider(),
        db_provider(),
        gateways_provider(),
        services_provider(),
        interactors_provider(),
    )


def init_async_container() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
