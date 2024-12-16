from dataclasses import dataclass

from cats.application.breed.gateway import BreedFilters, BreedReader
from cats.application.common.dto import Pagination
from cats.application.common.interactor import Interactor
from cats.entities.breed.models import Breed


@dataclass(frozen=True)
class GetBreedsInput:
    pagination: Pagination
    filters: BreedFilters


class GetBreeds(Interactor[GetBreedsInput, list[Breed]]):
    def __init__(self, breed_reader: BreedReader) -> None:
        self._breed_reader = breed_reader

    async def run(self, data: GetBreedsInput) -> list[Breed]:
        return await self._breed_reader.all(data.filters, data.pagination)
