from abc import abstractmethod
from typing import Any, Protocol


class UoWProtocol(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def refresh(self, instance: object) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> Any: ...

    @abstractmethod
    async def __aexit__(
        self,
        type_: type[BaseException],
        value: BaseException,
        traceback: None,
    ) -> Any: ...
