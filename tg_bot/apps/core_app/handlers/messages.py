from loguru import logger
from typing import Annotated
from aiogram import types, Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from aiogram3_di import Depends

from core.db import get_session, engine
from apps.users.models.users import User

core_router = Router(name="telegram")


@core_router.message(Command("id"))
async def cmd_id(message: Message, state: FSMContext) -> None:
    await message.answer(f"Your ID: {message.from_user.id}")


@core_router.message(CommandStart())
async def cmd_start(
    message: Message,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> None:
    r = await session.exec(
        select(User)
    )
    for t in r:
        print(t)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@core_router.message(F.text == "echo")
async def echo(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


@core_router.message(F.text == "ping")
async def hello(message: types.Message) -> None:
    try:
        await message.answer("pong")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")
