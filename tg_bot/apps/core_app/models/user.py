from sqlmodel import SQLModel, Field




class FastApiUserBase(SQLModel):
    name: str


class FastApiUser(FastApiUserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pass
