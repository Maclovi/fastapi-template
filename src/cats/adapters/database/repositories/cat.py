from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import breeds_table, cats_table
from cats.domain.models import Cat
from cats.domain.models.breed import Breed
from cats.domain.protocols.cat import CatRepositoryProtocol


class CatRepository(CatRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _load_cat(self, row: Row[Any]) -> Cat:
        return Cat(
            id=row.id,
            color=row.color,
            age=row.age,
            description=row.description,
            breed=Breed(row.title, id=row.breed_id) if row.title else None,
        )

    def _load_cats(self, rows: Sequence[Row[Any]]) -> list[Cat]:
        return [self._load_cat(row) for row in rows]

    async def get_all(self) -> list[Cat]:
        stmt = select(cats_table, breeds_table.c.title).join(
            breeds_table, isouter=True
        )
        result = await self._session.execute(stmt)

        return self._load_cats(result.all())

    async def get_by_breed(self, breed: str) -> list[Cat]:
        stmt = (
            select(cats_table, breeds_table.c.title)
            .join(breeds_table, isouter=True)
            .where(breeds_table.c.title == breed)
        )
        result = await self._session.execute(stmt)

        return self._load_cats(result.all())

    async def get_by_id(self, id: int) -> Cat | None:
        stmt = (
            select(cats_table, breeds_table.c.title)
            .join(breeds_table, isouter=True)
            .where(cats_table.c.id == id)
        )
        result = (await self._session.execute(stmt)).one_or_none()

        return self._load_cat(result) if result else None

    async def add(self, cat: Cat) -> None:
        stmt = cats_table.insert().values(
            id=cat.id,
            color=cat.color,
            age=cat.age,
            description=cat.description,
            breed_id=cat.breed.id if cat.breed else None,
        )
        await self._session.execute(stmt)

    async def update(self, cat: Cat) -> None:
        del cat.breed
        await self._session.merge(cat)

    async def delete_by_id(self, id: int) -> None:
        stmt = cats_table.delete().where(cats_table.c.id == id)
        await self._session.execute(stmt)
