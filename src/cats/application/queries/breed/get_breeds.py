from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed


@dataclass(frozen=True)
class GetBreedsQuery:
    pagination: Pagination


class GetBreedsQueryHandler(Interactor[GetBreedsQuery, list[Breed]]):
    def __init__(self, breed_gateway: BreedGateway) -> None:
        self._breed_gateway = breed_gateway

    async def run(self, data: GetBreedsQuery) -> list[Breed]:
        return await self._breed_gateway.all(data.pagination)
