from redis.asyncio.connection import ConnectionPool

from config.settings import get_settings

cfg = get_settings()

pool = ConnectionPool.from_url(cfg.redis_url)
