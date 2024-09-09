import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from config.settings import get_settings
from apps.users.models import users
from core.db import engine, get_session

cfg = get_settings()


secret_key_jwt = cfg.secret_key_jwt
algorythm_jwt = cfg.algorythm_jwt
ACCESS_TOKEN_EXPIRE_MINUTES = 1200


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_superuser_key(
        key: str,
        data: users.UserLogin,
        session: Annotated[AsyncSession, Depends(get_session)]
        ):
    if not cfg.debug or key != cfg.superuser_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect superuser_key"
        )
    superuser = users.User(
        is_superuser=True,
        username=data.username,
        password=get_password_hash(data.password)
    )
    session.add(superuser)
    await session.commit()
    await session.refresh(superuser)
    return superuser


async def get_user(username: str):
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as sesssion:
        user = await sesssion.exec(
            select(users.User).where(users.User.username == username)
        )
        user = user.first()
    return user


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        secret_key_jwt,
        algorithm=algorythm_jwt
    )
    return encoded_jwt


async def get_user_token(username: str, password: str) -> users.Token:
    user: users.User = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    return users.Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key_jwt, algorithms=[algorythm_jwt])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = users.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[users.User, Depends(get_current_user)],
):
    print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_superuser(
    current_user: Annotated[users.User, Depends(get_current_active_user)],
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not Superuser")
    return current_user
