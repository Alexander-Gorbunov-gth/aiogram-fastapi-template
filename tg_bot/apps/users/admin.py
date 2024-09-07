from typing import Any, Coroutine
from fastapi import Request
from sqladmin import ModelView

from .models.tg_user import TgUser
from .models.users import User
from core.admin import admin_site
from core.auth import get_password_hash


@admin_site.reg
class TgUserAdmin(ModelView, model=TgUser):
    column_list = [TgUser.name, TgUser.tg_id, TgUser.tg_username]
    name = "Пользователь бота"
    name_plural = "Пользователи бота"
    category = "Пользователи"
    page_size = 50


@admin_site.reg
class UserAdmin(ModelView, model=User):
    column_exclude_list = [User.id]
    column_searchable_list = [User.username]
    name = "Пользователь сайта"
    name_plural = "Пользователи сайта"
    category = "Пользователи"
    page_size = 50
    column_formatters = {
        User.password: lambda m, a: f"{m.password[:10]}************"
    }
    column_formatters_detail = {
        User.password: lambda m, a: m.password[:10]
    }
    
    async def on_model_change(
            self,
            data: dict,
            model: User,
            is_created: bool,
            request: Request
    ) -> Coroutine[Any, Any, None]:
        # Если создаем - просто меняем пароль на хэш пароль
        if is_created:  
            user_password = data["password"]
            password_hash = get_password_hash(user_password)
            data["password"] = password_hash
            return await super().on_model_change(data, model, is_created, request)
        # При редактировании проверяем редактровался ли пароль
        # Если да - сохраняем хэш 
        old_password_hash = model.password
        new_password = data["password"]
        if old_password_hash != new_password:
            password_hash = get_password_hash(new_password)
            data["password"] = password_hash
        return await super().on_model_change(data, model, is_created, request)