from dataclasses import dataclass

from cats.application.common.errors.base import ApplicationError


@dataclass(eq=False)
class BreedNotFoundError(ApplicationError):
    id: int

    @property
    def message(self) -> str:
        return f"Breed with id={self.id} not found"


@dataclass(eq=False)
class BreedNotFoundWithTitleError(ApplicationError):
    breed_title: str

    @property
    def message(self) -> str:
        return f"Breed with title={self.breed_title} not found"
