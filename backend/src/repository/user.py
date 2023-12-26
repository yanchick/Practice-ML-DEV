from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session_manager import get_session_maker
from src.database.user import User


class UserRepository:
    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession | None = None) -> User:
        should_close_session = session is None
        if session is None:
            session = await get_session_maker()
            await session.begin()
        query = select(User).where(User.username == username)
        result = (await session.scalars(query)).first()
        if should_close_session:
            await session.close()
        return result

    @staticmethod
    async def create_user(username: str, password: str, session: AsyncSession) -> User:
        user = User(username=username, password=password)
        session.add(user)
        await session.commit()
        return user
