from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Config(BaseConfig):
    DJANGO_SECRET: str
    EXTERNAL_API_KEY: str
    EXTERNAL_API_URL: str

    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int


config = Config()
