from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.breed import BreedFilters, BreedReader
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed


@dataclass(frozen=True)
class GetBreedsQuery:
    pagination: Pagination
    filters: BreedFilters


class GetBreedsQueryHandler(Interactor[GetBreedsQuery, list[Breed]]):
    def __init__(self, breed_reader: BreedReader) -> None:
        self._breed_reader = breed_reader

    async def run(self, data: GetBreedsQuery) -> list[Breed]:
        return await self._breed_reader.all(data.filters, data.pagination)
