from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from cats.domain.models import Breed, Cat

mapper_registry = registry()

breeds_table = Table(
    "breeds",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(30), nullable=False, unique=True),
)

cats_table = Table(
    "cats",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("color", String(30), nullable=False),
    Column("age", Integer, nullable=False),
    Column("description", String(200), nullable=False),
    Column(
        "breed_id",
        Integer,
        ForeignKey("breeds.id", ondelete="SET NULL"),
        nullable=True,
    ),
)


mapper_registry.map_imperatively(Breed, breeds_table)
mapper_registry.map_imperatively(
    Cat, cats_table, properties={"breed": relationship("Breed")}
)
