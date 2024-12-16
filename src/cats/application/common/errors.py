from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Application error"

    def __str__(self) -> str:
        return self.message
