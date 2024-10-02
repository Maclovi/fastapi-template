from cats.domain.models import Cat
from cats.domain.protocols import CatRepositoryProtocol, UoWProtocol


class CatService:
    """Cat service. The service layer is responsible for the business logic."""

    def __init__(
        self, repository: CatRepositoryProtocol, uow: UoWProtocol
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def get_all(self) -> list[Cat]:
        results: list[Cat] = await self._repository.get_all()
        return results

    async def get_by_breed(self, breed: str) -> list[Cat]:
        results: list[Cat] = await self._repository.get_by_breed(breed)
        return results

    async def get_by_id(self, id: int) -> Cat | None:
        return await self._repository.get_by_id(id)

    async def add(self, cat: Cat) -> None:
        async with self._uow:
            await self._repository.add(cat)
            await self._uow.commit()

    async def update(self, cat: Cat) -> None:
        async with self._uow:
            await self._repository.update(cat)
            await self._uow.commit()

    async def delete_by_id(self, id: int) -> None:
        async with self._uow:
            await self._repository.delete_by_id(id)
            await self._uow.commit()
