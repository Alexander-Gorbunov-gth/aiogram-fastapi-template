from functools import lru_cache
from venv import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final


@final
class Settings(BaseSettings):
    logger.info("test")
    model_config = SettingsConfigDict(
        env_file=(
            # '.dev.env',
            '.env'
        ),  # first search .dev.env, then .prod.env
        env_file_encoding='utf-8',
    )
    debug: bool = True
    redis_url: str = "redis://localhost:6379"
    test: str = "test"
    bot_token: str
    base_webhook_url: str
    db_url: str
    webhook_path: str = '/path/to/webhook'
    telegram_my_token: str
    admin_tg_id: int
    secret_key_jwt: str
    algorythm_jwt: str


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    logger.debug("get_settings")
    logger.debug(Settings())
    return Settings()
