from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger

import handlers # noqa, get handlers for Telegram
from core.route import root_router
from apps.logs.route import log_router
from config.settings import get_settings

cfg = get_settings()


async def _include_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(log_router)


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting application")
    from core.bot import start_telegram
    await start_telegram()
    await _include_routers(application)
    yield
    logger.info("⛔ Stopping application")

