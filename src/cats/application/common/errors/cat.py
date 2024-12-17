from dataclasses import dataclass

from cats.application.common.errors.base import ApplicationError


@dataclass(eq=False)
class CatNotFoundError(ApplicationError):
    id: int

    @property
    def message(self) -> str:
        return f"Cat with id={self.id} not found"


@dataclass(eq=False)
class CatIDNotFoundError(ApplicationError):
    @property
    def message(self) -> str:
        return "Cat id is None, should be an integer"
