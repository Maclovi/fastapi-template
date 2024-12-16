from cats.infrastructure.persistence.models.breed import map_breed_table
from cats.infrastructure.persistence.models.cat import map_cat_table


def map_tables() -> None:
    map_breed_table()
    map_cat_table()
