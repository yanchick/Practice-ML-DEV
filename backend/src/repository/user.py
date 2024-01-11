from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.user import User


class UserRepository:
    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
        query = select(User).where(User.username == username)
        result = (await session.scalars(query)).first()
        return result

    @staticmethod
    async def create_user(username: str, password: str, session: AsyncSession) -> User:
        user = User(username=username, password=password)
        session.add(user)
        await session.commit()
        return user
