import sys
from pathlib import Path
from abc import ABC, abstractmethod

from sqlalchemy import insert, select

sys.path.append(str(Path(__file__).resolve().parents[2]))
from infrastructure.database.utils import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self):
        raise NotImplementedError

    @abstractmethod
    async def find_by_options(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
    
    async def find_by_options(self, unique: bool = False, **kwargs):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**kwargs)
            results = await session.execute(stmt)
            if unique:
                results = results.scalar_one_or_none()
            else:
                results = results.scalars().all()
            return results
