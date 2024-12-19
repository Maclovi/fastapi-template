from cats.entities.breed.models import BreedID
from cats.entities.cat.models import Cat
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.tracker import Tracker


class CatService:
    def __init__(self, tracker: Tracker) -> None:
        self._tracker = tracker

    def add_cat(
        self,
        breed_id: BreedID | None,
        age: CatAge,
        color: CatColor,
        description: CatDescription,
    ) -> Cat:
        new_cat = Cat(
            oid=None,
            breed_id=breed_id,
            age=age,
            color=color,
            description=description,
        )
        self._tracker.add_one(new_cat)
        return new_cat

    def change_description(self, cat: Cat, new: CatDescription) -> None:
        cat.description = new

    async def remove_cat(self, cat: Cat) -> None:
        await self._tracker.delete(cat)
