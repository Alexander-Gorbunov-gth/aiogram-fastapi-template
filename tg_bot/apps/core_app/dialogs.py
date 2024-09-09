from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from .getters import username_getter
from .states import StartSG

start_dialog = Dialog(
    Window(
        Format('Привет, @{username}!'),
        getter=username_getter,
        state=StartSG.start
    ),
)
