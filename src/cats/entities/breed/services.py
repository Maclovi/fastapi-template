from cats.entities.breed.models import Breed
from cats.entities.breed.value_objects import BreedName
from cats.entities.common.tracker import Tracker


class BreedService:
    def __init__(self, tracker: Tracker) -> None:
        self._tracker = tracker

    def add_breed(self, name: BreedName) -> Breed:
        new_breed = Breed(oid=None, name=name)
        self._tracker.add_one(new_breed)
        return new_breed

    async def remove_breed(self, breed: Breed) -> None:
        await self._tracker.delete(breed)
