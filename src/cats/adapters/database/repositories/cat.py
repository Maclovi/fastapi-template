from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.adapters.database.models import cats
from cats.domain.models import Cat
from cats.domain.protocols.cat import CatRepositoryProtocol


class CatRepository(CatRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_cats(self) -> list[Cat]:
        stmt = select(cats)
        recieved_cats = await self.session.execute(stmt)
        return list(recieved_cats.scalars().all())

    async def get_by_breed(self, breed: str) -> list[Cat]:
        stmt = select(cats).where(cats.c.breed == breed)
        recieved_cats = await self.session.execute(stmt)
        return list(recieved_cats.scalars().all())

    async def get_by_id(self, id: int) -> Cat | None:
        stmt = select(cats).where(cats.c.id == id)
        recieved_cat = (await self.session.execute(stmt)).scalar()
        return recieved_cat if recieved_cat else None

    async def add(self, cat: Cat) -> Cat:
        async with self.session.begin():
            self.session.add(cat)
        return cat

    async def update(self, cat: Cat) -> Cat:
        async with self.session.begin():
            await self.session.merge(cat)
        return cat

    async def delete_by_id(self, id: int) -> None:
        stmt = select(cats).where(cats.c.id == id)
        async with self.session.begin():
            await self.session.execute(stmt)
