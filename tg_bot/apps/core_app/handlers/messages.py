from loguru import logger
from typing import Annotated, Tuple
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession
from aiogram3_di import Depends
from aiogram_dialog import DialogManager, StartMode

from core.db import get_session
from apps.users.models.tg_user import TgUser
from utils.db import update_or_create
from ..states import StartSG

from ..dialogs import start_dialog

core_router = Router(name="telegram")
core_router.include_router(start_dialog)


@core_router.message(Command("id"))
async def cmd_id(message: Message, state: FSMContext) -> None:
    await message.answer(f"Your ID: {message.from_user.id}")


@core_router.message(CommandStart())
async def cmd_start(
    message: Message,
    dialog_manager: DialogManager,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> None:
    data = {
        "tg_id": message.from_user.id,
        "tg_username": message.from_user.username,
        "name": message.from_user.full_name
    }
    user: TgUser
    user, is_create = await update_or_create(
        session,
        TgUser,
        data,
        "tg_id"
    )
    logger.info(f"{user.tg_username} is create {is_create}")
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
