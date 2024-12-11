from dataclasses import dataclass

from cats.entities.common.errors import DomainError


@dataclass(eq=False)
class AgeMaxError(DomainError):
    age: int

    @property
    def message(self) -> str:
        return f"Max age should be a less rhan {self.age!r}"


@dataclass(eq=False)
class ColorLengthError(DomainError):
    length: int

    @property
    def message(self) -> str:
        return f"Length of color should be a less than {self.length!r}"


@dataclass(eq=False)
class DescriptionLengthError(DomainError):
    length: int

    @property
    def message(self) -> str:
        return f"Length of description should be a less than {self.length!r}"
