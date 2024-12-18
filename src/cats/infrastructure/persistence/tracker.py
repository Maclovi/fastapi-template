from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from cats.entities.common.base_entity import BaseEntity, OIDType
from cats.entities.common.tracker import Tracker


class SATracker(Tracker):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add_one(self, entity: BaseEntity[OIDType]) -> None:
        self.session.add(entity)

    def add_many(self, entities: Iterable[BaseEntity[OIDType]]) -> None:
        self.session.add_all(entities)

    async def delete(self, entity: BaseEntity[OIDType]) -> None:
        await self.session.delete(entity)
