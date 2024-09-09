from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    """Стартовое состояние"""
    start = State()
