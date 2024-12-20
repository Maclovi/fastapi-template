import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from cats.entities.cat.models import Cat
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.infrastructure.persistence.models.base import mapper_registry

cats_table = sa.Table(
    "cats",
    mapper_registry.metadata,
    sa.Column("cat_id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("cat_age", sa.Integer, nullable=False),
    sa.Column("cat_color", sa.String(50), nullable=False),
    sa.Column("cat_description", sa.String(1000), nullable=False),
    sa.Column(
        "breed_id",
        sa.BigInteger,
        sa.ForeignKey("breeds.breed_id", ondelete="SET NULL"),
        nullable=True,
    ),
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


def map_cat_table() -> None:
    mapper_registry.map_imperatively(
        Cat,
        cats_table,
        properties={
            "oid": cats_table.c.cat_id,
            "breed": relationship(
                "Breed", back_populates="cats", lazy="joined"
            ),
            "age": composite(CatAge, cats_table.c.cat_age),
            "color": composite(CatColor, cats_table.c.cat_color),
            "description": composite(
                CatDescription, cats_table.c.cat_description
            ),
        },
    )
