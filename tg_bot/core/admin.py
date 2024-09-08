from pathlib import Path

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from fastapi import HTTPException

from core.db import engine
from .system import ImportModule
from apps.users.models import users
from core.auth import get_user_token, get_user, get_current_user


class AdminSite:

    def __init__(self) -> None:
        self.admin_views: list = []

    def reg(self, veiw_class: ModelView) -> ModelView:
        self.admin_views.append(veiw_class)
        return veiw_class


admin_site = AdminSite()


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        data = await request.form()
        user_data = users.UserLogin(**data)
        try:
            access_token: users.Token = await get_user_token(
                user_data.username,
                user_data.password
            )
            current_user: users.User = await get_user(
                username=user_data.username
            )
            if not current_user.is_superuser:
                return False
            request.session.update(
                {
                    "token": access_token.access_token,
                    "hash_pass": current_user.password
                }
            )
            return True
        except HTTPException:
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        hash_pass = request.session.get("hash_pass")
        user: users.User = await get_current_user(token)
        if not token:
            return False
        if user.password != hash_pass:
            return False
        if not user.is_superuser:
            return False
        return True


async def init_admin(app):
    """
    Добавлени все view с декоратором @reg для админки
    """
    authentication_backend = AdminAuth(secret_key="123")
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    apps = Path("apps")
    ImportModule.found_models_in_project(apps, "admin")
    for view in admin_site.admin_views:
        admin.add_view(view)
