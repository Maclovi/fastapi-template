from pydantic import BaseModel, Field

from cats.domain.models import Breed, Cat


class CatInput(BaseModel):
    id: int
    color: str
    age: int
    description: str
    breed: str | None = Field(default=None)

    def to_model(self) -> Cat:
        return Cat(
            id=self.id,
            color=self.color,
            age=self.age,
            description=self.description,
            breed=Breed(self.breed) if self.breed else None,
        )
