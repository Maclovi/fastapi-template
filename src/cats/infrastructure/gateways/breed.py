from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName
from cats.infrastructure.persistence.models.breed import breeds_table


class BreedMapper(BreedGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def with_id(self, breed_id: BreedID) -> Breed | None:
        stmt = select(Breed).where(breeds_table.c.breed_id == breed_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def with_name(self, name: BreedName) -> Breed | None:
        stmt = select(Breed).where(breeds_table.c.name == name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def all(self, pagination: Pagination) -> list[Breed]:
        stmt = select(Breed)
        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.offset(pagination.limit)
        result = await self._session.scalars(stmt)
        return [*result.all()]
