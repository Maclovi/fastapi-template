import logging

from cats.domain.models import Cat
from cats.domain.protocols import (
    BreedRepositoryProtocol,
    CatRepositoryProtocol,
    UoWProtocol,
)

logger = logging.getLogger(__name__)


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

    async def get_all(self) -> list[Cat]:
        results: list[Cat] = await self._cat_repository.get_all()
        return results

    async def get_by_breed(self, breed: str) -> list[Cat]:
        results: list[Cat] = await self._cat_repository.get_by_breed(breed)
        return results

    async def get_by_id(self, id: int) -> Cat | None:
        return await self._cat_repository.get_by_id(id)

    async def add(self, cat: Cat) -> None:
        if cat.breed:
            async with self._uow as nested_uow:
                try:
                    self._breed_repository.add(cat.breed)
                    await nested_uow.commit()
                except Exception as exc:
                    await nested_uow.rollback()
                    logger.error(exc)
                    breed = await self._breed_repository.get_by_title(
                        cat.breed.title
                    )
                    if breed:
                        cat.breed.id = breed.id

        await self._cat_repository.add(cat)
        await self._uow.commit()

    async def update(self, cat: Cat) -> None:
        # TODO: fix statement
        await self._cat_repository.update(cat)
        await self._uow.commit()

    async def delete_by_id(self, id: int) -> None:
        await self._cat_repository.delete_by_id(id)
        await self._uow.commit()
