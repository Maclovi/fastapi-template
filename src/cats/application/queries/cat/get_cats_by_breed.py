from dataclasses import dataclass
from typing import TypeAlias

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat

Output: TypeAlias = list[Cat] | None


@dataclass(frozen=True, slots=True)
class GetCatsWithBreedQuery:
    breed_name: str
    pagination: Pagination


class GetCatsWithBreedQueryHandler(Interactor[GetCatsWithBreedQuery, Output]):
    def __init__(self, cat_gateway: CatGateway) -> None:
        self._cat_gateway = cat_gateway

    async def run(self, data: GetCatsWithBreedQuery) -> Output:
        return await self._cat_gateway.with_breed_name(
            BreedName(data.breed_name), data.pagination
        )
