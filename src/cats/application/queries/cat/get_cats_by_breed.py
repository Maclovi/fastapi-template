from dataclasses import dataclass, field

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat


@dataclass(frozen=True, slots=True)
class GetCatsWithBreedQuery:
    breed_name: str
    pagination: Pagination = field(default_factory=Pagination)


class GetCatsWithBreedQueryHandler(
    Interactor[GetCatsWithBreedQuery, list[Cat]]
):
    def __init__(self, cat_gateway: CatGateway) -> None:
        self._cat_gateway = cat_gateway

    async def run(self, data: GetCatsWithBreedQuery) -> list[Cat]:
        return await self._cat_gateway.with_breed_name(
            BreedName(data.breed_name), data.pagination
        )
