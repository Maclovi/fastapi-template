from abc import abstractmethod
from typing import Protocol

from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName


class BreedGateway(Protocol):
    @abstractmethod
    async def with_id(self, breed_id: BreedID) -> Breed | None: ...

    @abstractmethod
    async def with_name(self, name: BreedName) -> Breed | None: ...

    @abstractmethod
    async def all(self, pagination: Pagination) -> list[Breed]: ...
