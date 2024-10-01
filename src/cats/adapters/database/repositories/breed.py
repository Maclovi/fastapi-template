from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import breeds
from cats.domain.models import Breed
from cats.domain.protocols import BreedRepositoryProtocol


class BreedRepository(BreedRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_breeds(self) -> list[Breed]:
        stmt = select(breeds)
        recieved_breeds = await self.session.execute(stmt)
        return list(recieved_breeds.scalars().all())
