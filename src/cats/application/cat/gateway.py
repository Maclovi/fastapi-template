from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

from cats.application.common.dto import Pagination
from cats.entities.breed.models import BreedId
from cats.entities.cat.models import Cat, CatId


@dataclass(frozen=True)
class CatFilters:
    breed_id: int | None = field(default=None)
    color: str | None = field(default=None)


class CatReader(Protocol):
    @abstractmethod
    async def all(
        self, filters: CatFilters, pagination: Pagination
    ) -> list[Cat]: ...

    @abstractmethod
    async def with_id(self, cat_id: CatId) -> Cat | None: ...

    @abstractmethod
    async def with_breed_id(
        self, breed: BreedId, filters: CatFilters
    ) -> None: ...


class CatSaver(Protocol):
    @abstractmethod
    async def save(self, cat: Cat) -> None: ...

    @abstractmethod
    async def update(self, cat: Cat) -> None: ...

    @abstractmethod
    async def delete_with_id(self, id: CatId) -> None: ...
