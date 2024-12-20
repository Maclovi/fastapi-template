from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Application error"

    def __str__(self) -> str:
        return self.message


@dataclass(eq=False)
class EntityNotFoundError(ApplicationError):
    @property
    def message(self) -> str:
        return "Entities are not equivalent"
