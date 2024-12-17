from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.breed import BreedReader
from cats.application.common.persistence.cat import CatFilters, CatReader
from cats.application.common.persistence.filters import Pagination
from cats.application.common.validators import validate_breed_with_title
from cats.entities.breed.value_objects import BreedTitle
from cats.entities.cat.models import Cat


@dataclass(frozen=True, slots=True)
class GetCatsQuery:
    breed_title: str
    pagination: Pagination


class GetCatsWithTitleCommandHandler(Interactor[GetCatsQuery, list[Cat]]):
    def __init__(
        self,
        cat_reader: CatReader,
        breed_reader: BreedReader,
    ) -> None:
        self._cat_reader = cat_reader
        self._breed_reader = breed_reader

    async def run(self, data: GetCatsQuery) -> list[Cat]:
        breed = await self._breed_reader.with_title(
            BreedTitle(data.breed_title)
        )
        assert validate_breed_with_title(breed)
        return await self._cat_reader.all(
            CatFilters(breed.id), pagination=data.pagination
        )
