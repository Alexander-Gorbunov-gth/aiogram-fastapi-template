from redis.asyncio.connection import ConnectionPool
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from config.settings import get_settings

cfg = get_settings()

pool = ConnectionPool.from_url(cfg.redis_url)

redis = Redis(host=cfg.redis_url)
storage = RedisStorage(redis=redis)
