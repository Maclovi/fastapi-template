from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry, relationship

from cats.domain.models import Breed, Cat

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)
mapper_registry = registry(metadata=metadata)

breeds_table = Table(
    "breeds",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(30), nullable=False, unique=True),
    Column(
        "created_at",
        DateTime,
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
        nullable=True,
    ),
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
    Column(
        "created_at",
        DateTime,
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
        nullable=True,
    ),
)


def map_tables() -> None:
    mapper_registry.map_imperatively(Breed, breeds_table)
    mapper_registry.map_imperatively(
        Cat, cats_table, properties={"breed": relationship("Breed")}
    )
