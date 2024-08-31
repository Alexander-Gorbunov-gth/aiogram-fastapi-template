from functools import lru_cache
from venv import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.dev.env', '.env'),  # first search .dev.env, then .prod.env
        env_file_encoding='utf-8',
    )
    debug: bool = True
    redis_url: str
    bot_token: str
    base_webhook_url: str
    db_url: str
    webhook_path: str = '/path/to/webhook'
    telegram_my_token: str
    admin_tg_id: int


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    logger.info(Settings().base_webhook_url)
    return Settings()
