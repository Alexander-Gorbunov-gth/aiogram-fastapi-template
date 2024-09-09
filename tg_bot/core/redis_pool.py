from redis.asyncio.connection import ConnectionPool
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio.client import Redis

from config.settings import get_settings

cfg = get_settings()

pool = ConnectionPool.from_url(cfg.redis_url)

redis = Redis.from_pool(pool)
storage = RedisStorage(
    redis=redis,
    key_builder=DefaultKeyBuilder(with_destiny=True)
)
