import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from cats.entities.breed.models import Breed
from cats.entities.breed.value_objects import BreedName
from cats.infrastructure.persistence.models.base import mapper_registry

breeds_table = sa.Table(
    "breeds",
    mapper_registry.metadata,
    sa.Column("breed_id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("breed_name", sa.String(50), nullable=False, unique=True),
    sa.Column(
        "created_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        server_onupdate=sa.func.now(),
        nullable=True,
    ),
)


def map_breed_table() -> None:
    mapper_registry.map_imperatively(
        Breed,
        breeds_table,
        properties={
            "oid": breeds_table.c.breed_id,
            "cats": relationship("Cat", back_populates="breed"),
            "name": composite(BreedName, breeds_table.c.breed_name),
        },
    )
