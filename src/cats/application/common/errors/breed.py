from dataclasses import dataclass

from cats.application.common.errors.base import EntityNotFoundError


@dataclass(eq=False)
class BreedNotFoundError(EntityNotFoundError):
    id: int

    @property
    def message(self) -> str:
        return f"Breed with id={self.id} not found"
