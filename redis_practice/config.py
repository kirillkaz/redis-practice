from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = Field(default=0)


config = Config()
