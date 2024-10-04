from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import breeds, cats
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
            breed=Breed(row.title) if row.title else None,
        )

    def _load_cats(self, rows: Sequence[Row[Any]]) -> list[Cat]:
        return [self._load_cat(row) for row in rows]

    async def get_all(self) -> list[Cat]:
        stmt = select(cats, breeds.c.title).join(breeds, isouter=True)
        result = await self._session.execute(stmt)

        return self._load_cats(result.all())

    async def get_by_breed(self, breed: str) -> list[Cat]:
        stmt = (
            select(cats, breeds.c.title)
            .join(breeds, isouter=True)
            .where(breeds.c.title == breed)
        )
        result = await self._session.execute(stmt)

        return self._load_cats(result.all())

    async def get_by_id(self, id: int) -> Cat | None:
        stmt = (
            select(cats, breeds.c.title)
            .join(breeds, isouter=True)
            .where(cats.c.id == id)
        )
        result = (await self._session.execute(stmt)).one_or_none()

        return self._load_cat(result) if result else None

    def add(self, cat: Cat) -> None:
        self._session.add(cat)

    async def update(self, cat: Cat) -> None:
        await self._session.merge(cat)

    async def delete_by_id(self, id: int) -> None:
        stmt = cats.delete().where(cats.c.id == id)
        await self._session.execute(stmt)
