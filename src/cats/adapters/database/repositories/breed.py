from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import breeds_table
from cats.domain.models import Breed
from cats.domain.protocols import BreedRepositoryProtocol


class BreedRepository(BreedRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _load_breed(self, row: Row[Any]) -> Breed:
        return Breed(id=row.id, title=row.title)

    def _load_breeds(self, rows: Sequence[Row[Any]]) -> list[Breed]:
        return [self._load_breed(row) for row in rows]

    def add(self, breed: Breed) -> None:
        self._session.add(breed)

    async def get_by_title(self, title: str) -> Breed | None:
        stmt = select(breeds_table).where(breeds_table.c.title == title)
        result = (await self._session.execute(stmt)).one_or_none()
        return self._load_breed(result) if result else None

    async def get_all(self) -> list[Breed]:
        stmt = select(breeds_table)
        recieved_breeds = await self._session.execute(stmt)
        return self._load_breeds(recieved_breeds.all())
