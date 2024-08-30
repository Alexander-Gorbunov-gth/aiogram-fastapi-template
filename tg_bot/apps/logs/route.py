from fastapi import APIRouter
from loguru import logger

from core.bot import bot
from . import base_model


log_router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    responses={404: {"description": "Not found"}},
)


@log_router.post("/send/")
async def send_log(log: base_model.Log) -> dict:
    await bot.send_message(log.id, log.text)
    return {"status": "Ok"}
