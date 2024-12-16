from pydantic import Field

from src.config.base import BaseConfig


class RedisConfig(BaseConfig):
    REDIS_DB: int = Field(default=0)
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)


redis_config = RedisConfig()