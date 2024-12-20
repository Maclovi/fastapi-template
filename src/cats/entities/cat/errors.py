from dataclasses import dataclass

from cats.entities.common.errors import FieldError


@dataclass(eq=False)
class CatAgeMaxError(FieldError):
    age: int

    @property
    def message(self) -> str:
        return f"Max age should be a less rhan {self.age!r}"


@dataclass(eq=False)
class CatColorLengthError(FieldError):
    length: int

    @property
    def message(self) -> str:
        return f"Length of color should be a less than {self.length!r}"


@dataclass(eq=False)
class CatDescriptionLengthError(FieldError):
    length: int

    @property
    def message(self) -> str:
        return f"Length of description should be a less than {self.length!r}"
