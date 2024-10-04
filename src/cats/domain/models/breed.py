from dataclasses import dataclass, field


@dataclass
class Breed:
    id: int = field(init=False)
    title: str
