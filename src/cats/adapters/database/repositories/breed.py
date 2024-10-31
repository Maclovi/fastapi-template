from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import breeds_table
from cats.domain.exceptions.breed_exc import BreedAlreadyExistError
from cats.domain.models import Breed
from cats.domain.protocols import BreedRepositoryProtocol


class BreedRepository(BreedRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, breed: Breed) -> None:
        self._session.add(breed)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise BreedAlreadyExistError from exc

    async def get_by_title(self, title: str) -> Breed | None:
        stmt = select(Breed).where(breeds_table.c.title == title)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Breed]:
        stmt = select(Breed)
        print(stmt)
        results = await self._session.scalars(stmt)
        return list(results.all())
