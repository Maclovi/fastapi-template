from abc import abstractmethod
from typing import Protocol

from cats.domain.models import Breed


class BreedRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_all(self) -> list[Breed]: ...
