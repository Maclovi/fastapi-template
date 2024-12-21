from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.cat import CatFilters, CatGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.cat.models import Cat


@dataclass(frozen=True, slots=True)
class GetCatsQuery:
    filters: CatFilters
    pagination: Pagination


class GetCatsQueryHandler(Interactor[GetCatsQuery, list[Cat]]):
    def __init__(self, cat_gateway: CatGateway) -> None:
        self._cat_gateway = cat_gateway

    async def run(self, data: GetCatsQuery) -> list[Cat]:
        return await self._cat_gateway.all(data.filters, data.pagination)
