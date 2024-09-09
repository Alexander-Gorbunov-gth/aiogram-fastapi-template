from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(unique=True)
    is_user: bool = Field(default=True)
    is_superuser: bool
    disabled: bool = False


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str

    def __str__(self) -> str:
        return f"User - {self.username}"


class UserInDB(UserBase):
    hashed_password: str


class UserPublic(UserBase):
    pass


class UserLogin(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
