from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedTitle


@dataclass(frozen=True)
class BreedFilters:
    breed_name: str | None = field(default=None)


class BreedReader(Protocol):
    @abstractmethod
    async def with_id(self, user_id: BreedID) -> Breed | None: ...

    @abstractmethod
    async def with_title(self, user_id: BreedTitle) -> Breed | None: ...

    @abstractmethod
    async def all(
        self, filters: BreedFilters, pagination: Pagination
    ) -> list[Breed]: ...

    @abstractmethod
    async def total(self, filters: BreedFilters) -> int: ...


class BreedSaver(Protocol):
    @abstractmethod
    async def save(self, user_id: Breed) -> None: ...
