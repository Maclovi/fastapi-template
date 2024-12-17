from dataclasses import dataclass, field

from cats.application.common.committer import Committer
from cats.application.common.interactor import Interactor
from cats.application.common.persistence.breed import BreedReader, BreedSaver
from cats.application.common.persistence.cat import CatSaver
from cats.application.common.validators import validate_cat_id
from cats.entities.breed.models import Breed
from cats.entities.breed.value_objects import BreedTitle
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@dataclass(frozen=True)
class AddCatCommand:
    age: int
    color: str
    description: str
    breed_title: str | None = field(default=None)


class AddCatCommandHandler(Interactor[AddCatCommand, CatID]):
    def __init__(
        self,
        committer: Committer,
        cat_saver: CatSaver,
        breed_reader: BreedReader,
        breed_saver: BreedSaver,
    ) -> None:
        self._committer = committer
        self._cat_saver = cat_saver
        self._breed_reader = breed_reader
        self._breed_saver = breed_saver

    async def run(self, data: AddCatCommand) -> CatID:
        breed_id = None
        if title := data.breed_title:
            breed = await self._breed_reader.with_title(BreedTitle(title))
            if breed is None:
                breed = Breed(id=None, title=BreedTitle(title))
                await self._breed_saver.save(breed)
                breed_id = breed.id
            else:
                breed_id = breed.id

        cat = Cat(
            id=None,
            breed_id=breed_id,
            age=CatAge(data.age),
            color=CatColor(data.color),
            description=CatDescription(data.description),
        )
        await self._cat_saver.save(cat)
        assert validate_cat_id(cat.id)
        return cat.id
