from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.model import Model


class ModelRepository:
    @staticmethod
    async def get_model_by_name(name: str, session: AsyncSession) -> Model | None:
        query = select(Model).where(Model.name == name)
        result = (await session.scalars(query)).first()
        return result

    @staticmethod
    async def get_model_by_id(model_id: int, session: AsyncSession) -> Model | None:
        query = select(Model).where(Model.id == model_id)
        result = (await session.scalars(query)).first()
        return result

    @staticmethod
    async def get_all_models(session: AsyncSession) -> list[Model] | None:
        query = select(Model)
        result = (await session.scalars(query)).all()
        return result  # type: ignore[return-value]
