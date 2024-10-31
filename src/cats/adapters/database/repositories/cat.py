from collections.abc import Sequence

from sqlalchemy import RowMapping, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import breeds_table, cats_table
from cats.domain.exceptions.cat_exc import CatAlreadyExistError
from cats.domain.models import Cat
from cats.domain.protocols.cat import CatRepositoryProtocol


class CatRepository(CatRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _load_cat(self, row: RowMapping) -> Cat:
        return Cat(
            id=row.id,
            color=row.color,
            age=row.age,
            description=row.description,
            breed_id=row.breed_id,
        )

    def _load_cats(self, rows: Sequence[RowMapping]) -> list[Cat]:
        return [self._load_cat(row) for row in rows]

    async def save(self, cat: Cat) -> None:
        self._session.add(cat)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise CatAlreadyExistError from exc

    async def get_all(self) -> list[Cat]:
        stmt = select(Cat)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_breed(self, breed: str) -> list[Cat]:
        stmt = (
            select(cats_table)
            .join(breeds_table, isouter=True)
            .where(breeds_table.c.title == breed)
        )
        result = await self._session.execute(stmt)
        return self._load_cats(result.mappings().all())

    async def get_by_id(self, id: int) -> Cat | None:
        stmt = (
            select(cats_table, breeds_table.c.title)
            .join(breeds_table, isouter=True)
            .where(cats_table.c.id == id)
        )
        result = await self._session.execute(stmt)
        row = result.mappings().one_or_none()
        if not row:
            return None
        return self._load_cat(row)

    async def update(self, cat: Cat) -> None:
        await self._session.merge(cat)

    async def delete_by_id(self, id: int) -> None:
        stmt = delete(Cat).where(cats_table.c.id == id)
        await self._session.execute(stmt)
