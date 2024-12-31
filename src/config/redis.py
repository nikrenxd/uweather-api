from pydantic import Field
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    REDIS_DB: int = Field(default=0)
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


redis_config = RedisConfig()
