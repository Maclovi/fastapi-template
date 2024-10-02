from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import breeds
from cats.domain.models import Breed
from cats.domain.protocols import BreedRepositoryProtocol


class BreedRepository(BreedRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _load_breed(self, row: Row[Any]) -> Breed:
        return Breed(id=row.id, title=row.title)

    def _load_breeds(self, rows: Sequence[Row[Any]]) -> list[Breed]:
        return [self._load_breed(row) for row in rows]

    async def get_all(self) -> list[Breed]:
        stmt = select(breeds)
        recieved_breeds = await self._session.execute(stmt)
        return self._load_breeds(recieved_breeds.all())
