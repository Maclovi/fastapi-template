import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from cats.domain.models import Breed
from cats.entities.breed.value_objects import BreedTitle
from cats.infrastructure.persistence.models.base import mapper_registry

breeds_table = sa.Table(
    "breeds",
    mapper_registry.metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("title", sa.String(50), nullable=False, unique=True),
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
            "cats": relationship("Cat", back_populates="breed"),
            "title": composite(BreedTitle, breeds_table.c.title),
        },
    )
