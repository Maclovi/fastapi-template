from abc import abstractmethod
from typing import Protocol

from cats.domain.models import Cat


class CatRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_all_cats(self) -> list[Cat]: ...

    @abstractmethod
    async def get_by_breed(self, breed: str) -> list[Cat]: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> Cat | None: ...

    @abstractmethod
    async def add(self, cat: Cat) -> Cat: ...

    @abstractmethod
    async def update(self, cat: Cat) -> Cat: ...

    @abstractmethod
    async def delete_by_id(self, id: int) -> None: ...