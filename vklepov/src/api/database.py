"""database setup."""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./drevil.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autocommit=False, autoflush=False
)


Base = declarative_base()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
