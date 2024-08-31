from sqladmin import ModelView

from .models.tg_user import TgUser
from core.admin import admin_site


@admin_site.reg
class UserAdmin(ModelView, model=TgUser):
    column_list = [TgUser.name, TgUser.tg_id, TgUser.tg_username]
