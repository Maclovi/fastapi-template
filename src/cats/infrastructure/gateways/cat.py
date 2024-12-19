from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.application.common.persistence.cat import CatFilters, CatGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat, CatID
from cats.infrastructure.persistence.models.breed import breeds_table
from cats.infrastructure.persistence.models.cat import cats_table


class CatMapper(CatGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def is_exist(self, cat_id: CatID) -> bool:
        query = select(exists().where(cats_table.c.cat_id == cat_id))
        result = await self._session.execute(query)
        return bool(result.scalar())

    async def with_id(self, cat_id: CatID) -> Cat | None:
        stmt = select(Cat).where(cats_table.c.cat_id == cat_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def with_breed_name(
        self, breed_name: BreedName, pagination: Pagination
    ) -> list[Cat]:
        stmt = (
            select(Cat)
            .join(
                breeds_table,
                cats_table.c.breed_id == breeds_table.c.breed_id,
                isouter=True,
            )
            .where(breeds_table.c.name == breed_name)
        )
        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.limit(pagination.limit)
        result = await self._session.scalars(stmt)
        return [*result.all()]

    async def all(
        self, filters: CatFilters, pagination: Pagination
    ) -> list[Cat]:
        stmt = select(Cat)
        if filters.breed_id:
            stmt = stmt.where(cats_table.c.breed_id == filters.breed_id)
        if filters.color:
            stmt = stmt.where(cats_table.c.color == filters.color)
        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.offset(pagination.limit)
        result = await self._session.scalars(stmt)
        return [*result.all()]
