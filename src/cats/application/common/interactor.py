from abc import abstractmethod
from typing import Protocol, TypeVar

InputData_contra = TypeVar("InputData_contra", contravariant=True)
OutputData_co = TypeVar("OutputData_co", covariant=True)


class Interactor(Protocol[InputData_contra, OutputData_co]):
    @abstractmethod
    async def run(self, data: InputData_contra) -> OutputData_co: ...
