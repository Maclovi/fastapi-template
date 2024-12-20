from dataclasses import dataclass

from cats.application.common.errors.base import EntityNotFoundError


@dataclass(eq=False)
class CatNotFoundError(EntityNotFoundError):
    id: int

    @property
    def message(self) -> str:
        return f"Cat with id={self.id} not found"
