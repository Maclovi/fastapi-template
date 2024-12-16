from dataclasses import dataclass

from cats.entities.common.errors import DomainError


@dataclass(eq=False)
class TitlelengthError(DomainError):
    length: int

    @property
    def message(self) -> str:
        return f"Length of title should be a less than {self.length!r}"
