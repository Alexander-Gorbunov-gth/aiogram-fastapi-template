from os import getppid
import redis.asyncio as aredis
from config.settings import get_settings
import importlib
from pathlib import Path

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


class ImportModule:
    """Импорт модулей из папок проекта"""

    @staticmethod
    def import_module(path: Path):
        if path.is_file():
            path = ".".join(path.parts)
            if path.endswith(".py"):
                path = path[:-3]
            importlib.import_module(path)
            return
        for file in path.iterdir():
            if file.is_file():
                path = ".".join(file.parts)
                if path.endswith(".py"):
                    path = path[:-3]
                importlib.import_module(path)

    @staticmethod
    def found_models_in_project(path: Path, search: str):
        if search in path.name:
            ImportModule.import_module(path)
            return
        if path.is_dir():
            for dir in path.iterdir():
                if "__pycache__" in dir.name:
                    continue
                ImportModule.found_models_in_project(dir, search)
