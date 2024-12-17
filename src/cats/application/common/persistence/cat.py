from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

from cats.application.common.persistence.filters import Pagination
from cats.entities.cat.models import Cat, CatID


@dataclass(frozen=True)
class CatFilters:
    breed_id: int | None = field(default=None)
    color: str | None = field(default=None)


class CatReader(Protocol):
    @abstractmethod
    async def with_id(self, cat_id: CatID) -> Cat | None: ...

    @abstractmethod
    async def all(
        self, filters: CatFilters, pagination: Pagination
    ) -> list[Cat]: ...


class CatSaver(Protocol):
    @abstractmethod
    async def save(self, cat: Cat) -> None: ...

    @abstractmethod
    async def update(self, cat: Cat) -> None: ...

    @abstractmethod
    async def delete_with_id(self, id: CatID) -> None: ...
