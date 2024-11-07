import logging
from dataclasses import dataclass

from cats.domain.models.breed import Breed, BreedId
from cats.domain.models.cat import Cat, CatId
from cats.domain.protocols import (
    BreedRepositoryProtocol,
    CatRepositoryProtocol,
    UoWProtocol,
)

logger = logging.getLogger(__name__)


@dataclass
class CatInputData:
    id: int
    color: str
    age: int
    description: str
    breed_title: str | None


class CatService:
    """Cat service. The service layer is responsible for the business logic."""

    def __init__(
        self,
        cat_repository: CatRepositoryProtocol,
        breed_repository: BreedRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self._cat_repository = cat_repository
        self._breed_repository = breed_repository
        self._uow = uow

    async def _get_breed_id(self, title: str | None) -> BreedId | None:
        breed_id = None
        if title:
            breed = await self._breed_repository.get_by_title(title)
            if breed is None:
                breed = Breed(title=title)
                await self._breed_repository.save(breed)
            breed_id = breed.id
        return breed_id

    async def _handle_data(self, data: CatInputData) -> Cat:
        breed_id = await self._get_breed_id(data.breed_title)
        return Cat(
            id=CatId(data.id),
            color=data.color,
            age=data.age,
            description=data.description,
            breed_id=breed_id,
        )

    async def get_all(self) -> list[Cat]:
        results: list[Cat] = await self._cat_repository.get_all()
        return results

    async def get_by_breed(self, breed: str) -> list[Cat]:
        results: list[Cat] = await self._cat_repository.get_by_breed(breed)
        return results

    async def get_by_id(self, id: int) -> Cat | None:
        return await self._cat_repository.get_by_id(id)

    async def add(self, data: CatInputData) -> CatId:
        cat = await self._handle_data(data)
        await self._cat_repository.save(cat)
        await self._uow.commit()
        return cat.id

    async def update(self, data: CatInputData) -> None:
        cat = await self._handle_data(data)
        await self._cat_repository.update(cat)
        await self._uow.commit()

    async def delete_by_id(self, id: int) -> None:
        await self._cat_repository.delete_by_id(id)
        await self._uow.commit()
