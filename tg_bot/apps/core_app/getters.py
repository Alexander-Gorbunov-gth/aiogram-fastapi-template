from aiogram_dialog import DialogManager
from aiogram.types import User


async def username_getter(
        dialog_manager: DialogManager,
        event_from_user: User, **kwargs):
    return {'username': event_from_user.username}
