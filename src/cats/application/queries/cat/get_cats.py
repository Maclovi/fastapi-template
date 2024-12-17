from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.cat import CatFilters, CatReader
from cats.application.common.persistence.filters import Pagination
from cats.entities.cat.models import Cat


@dataclass(frozen=True)
class GetCatsQuery:
    pagination: Pagination
    filters: CatFilters


class GetCatsQueryHandler(Interactor[GetCatsQuery, list[Cat]]):
    def __init__(self, cat_reader: CatReader) -> None:
        self._cat_reader = cat_reader

    async def run(self, data: GetCatsQuery) -> list[Cat]:
        return await self._cat_reader.all(data.filters, data.pagination)
