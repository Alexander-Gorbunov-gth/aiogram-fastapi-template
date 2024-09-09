from typing import Tuple

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.exc import NoResultFound

from sqlmodel import select


async def update_or_create(
        session: AsyncSession,
        model: SQLModel,
        data: dict,
        search: str
) -> Tuple[SQLModel, bool]:
    try:
        obj = await session.exec(
            select(model).where(getattr(model, search) == data[search])
        )
        obj = obj.one()
        del data[search]
        for key, value in data.items():
            setattr(obj, key, value)
        is_create = False
    except NoResultFound:
        obj = model(**data)
        is_create = True
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj, is_create
