from sqlalchemy import select, update
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

    @staticmethod
    async def subtract_money(user_id: int, cost: float, session: AsyncSession) -> None:
        await session.execute(update(User).where(User.id == user_id).values(balance=User.balance - cost))
        await session.commit()
