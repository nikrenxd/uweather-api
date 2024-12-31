from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    DB_NAME: str = Field(default="postgres")
    DB_USER: str = Field(default="postgres")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_PASSWORD: str = Field(default="postgres")


db_config = DatabaseConfig()
