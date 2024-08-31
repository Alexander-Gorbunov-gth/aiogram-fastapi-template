from os import getppid
import redis.asyncio as aredis
from config.settings import get_settings

cfg = get_settings()


async def first_run() -> bool:
    ppid = getppid()
    redis = await aredis.from_url(cfg.redis_url)
    save_pid = await redis.get('tg_bot_ppid')
    if save_pid and int(save_pid) == ppid:
        await redis.close()
        return False
    await redis.set('tg_bot_ppid', ppid)
    await redis.close()
    return True
