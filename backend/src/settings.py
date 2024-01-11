from typing import Any

from pydantic import Field, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_db: str
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str
    postgres_password: str

    redis_password: str
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)

    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str = Field(default="88088d1326a9357804caf831f8c7d97d3d04dcffbf36c1c382486cec6f22f564")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60 * 24 * 3)  # default 3 days

    debug: bool = Field(default=False)
    host: IPvAnyAddress = Field(default=IPvAnyAddress("127.0.0.1"))
    port: int = Field(default=8000)

    @property
    def database_settings(self) -> Any:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.postgres_db,
            "user": self.postgres_user,
            "password": self.postgres_password,
            "host": self.postgres_host,
            "port": self.postgres_port,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def redis_url(self) -> str:
        """
        Get uri for connection with redis.
        """
        return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/0"
