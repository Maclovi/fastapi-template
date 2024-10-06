from dataclasses import dataclass, field


@dataclass
class Breed:
    title: str
    id: int | None = field(default=None)
