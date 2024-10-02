from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from cats.domain.models import Breed, Cat

mapper_registry = registry()

cats = Table(
    "cats",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("color", String),
    Column("age", Integer),
    Column("description", String),
    Column(
        "breed_id", ForeignKey("breeds.id", ondelete="CASCADE"), nullable=True
    ),
)

breeds = Table(
    "breeds",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
)

mapper_registry.map_imperatively(Breed, breeds)
mapper_registry.map_imperatively(
    Cat, cats, properties={"breed": relationship(Breed)}
)
