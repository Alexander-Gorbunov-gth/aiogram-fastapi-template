import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger
from sqladmin import Admin

from core.route import root_router
from apps.logs.route import log_router
from config.settings import get_settings
from .admin import init_admin



cfg = get_settings()


async def _include_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(log_router)



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting application")
    from core.bot import start_telegram
    await start_telegram()
    await _include_routers(app)
    await init_admin(app)
    yield
    logger.info("⛔ Stopping application")
