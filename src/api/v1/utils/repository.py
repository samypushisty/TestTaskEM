from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from api.v1.base_schemas.schemas import StandartException

import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


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
            logger.debug("Success")
            return stmt
        except:
            logger.error("Invalid data")
            raise StandartException(status_code=400, detail="Invalid data")


    async def find(self, session: AsyncSession, validate: bool = False,**filters):
        query = (
            select(self.model)
            .filter_by(**filters)
        )
        result = await session.execute(query)
        result = result.scalars().first()
        if not result and validate:
            logger.error("Not found")
            raise StandartException(status_code=404, detail="not found")
        logger.debug("Success")
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
            logger.error("Not found")
            raise StandartException(status_code=404, detail="not found")
        logger.debug("Success")
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
            logger.error("Not found")
            raise StandartException(status_code=404, detail="not found")
        logger.debug("Success")
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
            logger.error("Invalid data")
            raise StandartException(status_code=400, detail="Invalid data")
        if result.rowcount == 0:
            logger.error("Not found")
            raise StandartException(status_code=404, detail="not found")
        logger.debug("Success")
        await session.flush()

    async def patch_field(self, session: AsyncSession, field: str, value: Any, **filters):
        stmt = (
            update(self.model)
            .values({field : value})
            .filter_by(**filters)
        )
        try:
            result = await session.execute(stmt)
            if result.rowcount == 0:
                logger.error("Not found")
                raise StandartException(status_code=404, detail="Not Found")
        except:
            logger.error("Invalid data")
            raise StandartException(status_code=400, detail="Invalid data")
        logger.debug("Success")
        await session.flush()

    async def delete(self, session: AsyncSession,validate = True,**filters):
        query = (
            delete(self.model)
            .filter_by(**filters)
        )
        result = await session.execute(query)
        if result.rowcount == 0 and validate:
            logger.error("Not found")
            raise StandartException(status_code=404, detail="not found")
        logger.debug("Success")
        await session.flush()
