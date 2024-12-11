from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):
    @property
    def message(self) -> str:
        return "Domain Error"

    def __str__(self) -> str:
        return self.message


@dataclass(eq=False)
class EntityError(DomainError):
    @property
    def message(self) -> str:
        return "Entities are not equivalent"
