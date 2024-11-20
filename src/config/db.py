from pydantic import Field

from src.config.base import BaseConfig


class DatabaseConfig(BaseConfig):
    DB_NAME: str = Field(default="postgres")
    DB_USER: str = Field(default="postgres")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_PASSWORD: str = Field(default="postgres")


db_config = DatabaseConfig()