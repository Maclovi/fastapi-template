from dataclasses import dataclass

from cats.application.common.errors.base import ApplicationError


@dataclass(eq=False)
class BreedNotFoundError(ApplicationError):
    id: int

    @property
    def message(self) -> str:
        return f"Breed with id={self.id} not found"
