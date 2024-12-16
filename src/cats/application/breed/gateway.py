from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

from cats.application.common.dto import Pagination
from cats.entities.breed.models import Breed, BreedId


@dataclass(frozen=True)
class BreedFilters:
    breed_name: str | None = field(default=None)


class BreedReader(Protocol):
    @abstractmethod
    async def with_id(self, user_id: BreedId) -> Breed | None: ...

    @abstractmethod
    async def all(
        self, filters: BreedFilters, pagination: Pagination
    ) -> list[Breed]: ...

    @abstractmethod
    async def total(self, filters: BreedFilters) -> int: ...
