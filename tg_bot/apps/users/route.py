from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter

from apps.users.models import users
from core.auth import (get_user_token,
                       get_current_active_user,
                       create_superuser_key
                       )
from config.settings import get_settings

cfg = get_settings()


auth_router = APIRouter(
    prefix="",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post("/api/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> users.Token:
    token = await get_user_token(form_data.username, form_data.password)
    return token


@auth_router.post("/login/")
async def login_for_access_token_with_api(
    data: users.UserLogin
):
    token = await get_user_token(data.username, data.password)
    return token


@auth_router.post(
        "/create-superuser/",
        include_in_schema=cfg.debug)
async def create_superuser(
    superuser: Annotated[users.User, Depends(create_superuser_key)],
):
    return superuser


@auth_router.get("/users/me/", response_model=users.UserPublic)
async def read_users_me(
    current_user: Annotated[users.User, Depends(get_current_active_user)],
):
    return current_user
