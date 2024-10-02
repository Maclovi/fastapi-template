from abc import abstractmethod
from typing import Protocol


class UoWProtocol(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> None: ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: None,
    ) -> None: ...
