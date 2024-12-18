from dataclasses import dataclass

from cats.application.common.errors.base import ApplicationError


@dataclass(eq=False)
class CatNotFoundError(ApplicationError):
    id: int

    @property
    def message(self) -> str:
        return f"Cat with id={self.id} not found"
