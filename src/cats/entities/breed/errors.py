from dataclasses import dataclass

from cats.entities.common.errors import FieldError


@dataclass(eq=False)
class BreedNamelengthError(FieldError):
    length: int

    @property
    def message(self) -> str:
        return f"Length of title should be a less than {self.length!r}"
