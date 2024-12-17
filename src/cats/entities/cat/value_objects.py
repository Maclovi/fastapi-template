from dataclasses import dataclass, field

from cats.entities.cat.errors import (
    AgeMaxError,
    ColorLengthError,
    DescriptionLengthError,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatAge:
    value: int

    MAX_AGE: int = field(init=False, default=99)

    def __post_init__(self) -> None:
        if self.value > self.MAX_AGE:
            raise AgeMaxError(self.value)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatColor:
    value: str

    MIN_LENGTH: int = field(init=False, default=3)
    MAX_LENGTH: int = field(init=False, default=50)

    def __post_init__(self) -> None:
        if not (self.MIN_LENGTH <= len(self.value) <= self.MAX_LENGTH):
            raise ColorLengthError(self.MAX_LENGTH)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatDescription:
    value: str

    MAX_LENGTH: int = field(init=False, default=1000)

    def __post_init__(self) -> None:
        if len(self.value) > self.MAX_LENGTH:
            raise DescriptionLengthError(self.MAX_LENGTH)
