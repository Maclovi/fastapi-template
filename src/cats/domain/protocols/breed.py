from abc import abstractmethod
from typing import Protocol

from cats.domain.models import Breed


class BreedRepositoryProtocol(Protocol):
    @abstractmethod
    async def save(self, breed: Breed) -> None: ...

    @abstractmethod
    async def get_by_title(self, title: str) -> Breed | None: ...

    @abstractmethod
    async def get_all(self) -> list[Breed]: ...
