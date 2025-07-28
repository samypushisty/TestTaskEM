from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from api.api_v1.base_schemas.schemas import StandartException


class AbstractRepository(ABC):
    @abstractmethod
    async  def add(self, session: AsyncSession, data: dict):
        ...

    @abstractmethod
    async def find(self, session: AsyncSession, validate: bool = False,**filters):
        ...


    @abstractmethod
    async def find_all(self, session: AsyncSession, order_column: str, validate: bool = False, **filters):
        ...


    @abstractmethod
    async def find_paginated(self, session: AsyncSession, page: int, order_column: str, validate: bool = False, per_page: int = 20, **filters):
        ...


    @abstractmethod
    async def patch(self, session: AsyncSession, data: dict, **filters):
        ...


    @abstractmethod
    async def patch_field(self, session: AsyncSession, field: str, value: Decimal, **filters):
        ...


    @abstractmethod
    async def delete(self, session: AsyncSession,**filters):
        ...


class SQLAlchemyRepository(AbstractRepository):


    def __init__(self,model) -> None:
        self.model = model


    async def add(self, session: AsyncSession, data: dict):

        try:
            stmt = self.model(**data)
            session.add(stmt)
            await session.flush()
            return stmt
        except:
            raise StandartException(status_code=400, detail="Invalid data")


    async def find(self, session: AsyncSession, validate: bool = False,**filters):
        query = (
            select(self.model)
            .filter_by(**filters)
        )
        result = await session.execute(query)
        result = result.scalars().first()
        if not result and validate:
            raise StandartException(status_code=404, detail="not found")
        return result


    async def find_all(self, session: AsyncSession, order_column: str, validate: bool = False, **filters):
        query = (
            select(self.model)
            .filter_by(**filters)
            .order_by(getattr(self.model, order_column))
        )
        result = await session.execute(query)
        result = result.scalars().all()
        if not result and validate:
            raise StandartException(status_code=404, detail="not found")

        return result


    async def find_paginated(self, session: AsyncSession, page: int, order_column: str, validate: bool = False, per_page: int = 20, **filters):
        offset = (page - 1) * per_page
        query = (
            select(self.model)
            .filter_by(**filters)
            .order_by(getattr(self.model, order_column))
            .offset(offset)
            .limit(per_page)
        )
        result = await session.execute(query)
        result = result.scalars().all()
        if not result and validate:
            raise StandartException(status_code=404, detail="not found")
        return result


    async def patch(self, session: AsyncSession, data: dict, **filters):
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(**filters)
        )
        try:
            result = await session.execute(stmt)
        except:
            raise StandartException(status_code=400, detail="Invalid data")
        if result.rowcount == 0:
            raise StandartException(status_code=404, detail="not found")
        await session.flush()

    async def patch_field(self, session: AsyncSession, field: str, value: Any, **filters):
        stmt = (
            update(self.model)
            .values({field : value})
            .filter_by(**filters)
        )
        try:
            result = await session.execute(stmt)
            if validate and result.rowcount == 0:
                raise StandartException(status_code=404, detail="Not Found")
        except:
            raise StandartException(status_code=400, detail="Invalid data")
        await session.flush()

    async def delete(self, session: AsyncSession,validate = True,**filters):
        query = (
            delete(self.model)
            .filter_by(**filters)
        )
        result = await session.execute(query)
        if result.rowcount == 0 and validate:
            raise StandartException(status_code=404, detail="not found")
        await session.flush()
