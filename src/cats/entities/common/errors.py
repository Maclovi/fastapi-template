from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):
    @property
    def message(self) -> str:
        return "Domain error"

    def __str__(self) -> str:
        return self.message


@dataclass(eq=False)
class FieldError(DomainError):
    @property
    def message(self) -> str:
        return "Field error"


@dataclass(eq=False)
class EntityError(DomainError):
    @property
    def message(self) -> str:
        return "Entity error"


@dataclass(eq=False)
class InsertProcessingError(EntityError):
    @property
    def message(self) -> str:
        return "Insert processing error"
