import sys
from pathlib import Path
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

sys.path.append(str(Path(__file__).resolve().parents[2]))
from infrastructure.database.model import Base


SCRIPT_DIR = Path(__file__).parent
DB_ADDRESS = f'{SCRIPT_DIR}\\source\\mlpractice.db'


sync_engine = create_engine(f'sqlite:///{DB_ADDRESS}')
async_engine = create_async_engine(f'sqlite+aiosqlite:///{DB_ADDRESS}')
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


def init_db(engine=sync_engine):
    Base.metadata.create_all(bind=engine)
