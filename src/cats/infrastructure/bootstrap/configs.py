from dataclasses import dataclass
from os import environ as env


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    user: str
    password: str
    host: str
    port: int
    db_name: str
    debug: bool

    @property
    def uri(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass(frozen=True, slots=True)
class APIConfig:
    host: str
    port: int


@dataclass(frozen=True, slots=True)
class Configs:
    db: PostgresConfig
    api: APIConfig


def load_configs() -> Configs:
    return Configs(
        db=PostgresConfig(
            user=env["POSTGRES_USER"],
            password=env["POSTGRES_PASSWORD"],
            host=env["POSTGRES_HOST"],
            port=int(env["POSTGRES_PORT"]),
            db_name=env["POSTGRES_DB"],
            debug=env["POSTGRES_DEBUG"] == "true",
        ),
        api=APIConfig(
            host=env["UVICORN_HOST"],
            port=int(env["UVICORN_PORT"]),
        ),
    )
