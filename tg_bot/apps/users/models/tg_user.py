from sqlmodel import SQLModel, Field


class TgUserBase(SQLModel):
    name: str
    tg_id: str = Field(primary_key=True)
    tg_username: str | None


class TgUser(TgUserBase, table=True):
    pass
