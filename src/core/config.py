from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class RunConfig(BaseModel):
    host: str = 'localhost'
    port: int = 8000

class RedisConfig(BaseModel):
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_HOST: str = ""

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    user: str = "/user"
    manage: str = "/manage"
    post: str = "/post"
    settings: str = "/settings"


class ApiPrefix(BaseModel):
    prefix: str = "/api"

    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn = ""
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore"
    )
    default_permissions: list = ["create","edit","delete"]
    secret_key: str = ""
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    db_redis: RedisConfig =RedisConfig()

settings = Settings()

