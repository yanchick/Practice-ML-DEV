from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.infrastructure.database.model import Base, Models


SCRIPT_DIR = Path(__file__).parent
DB_ADDRESS = f'{SCRIPT_DIR}\\source\\mydatabase.db'


sync_engine = create_engine(f'sqlite:///{DB_ADDRESS}')
async_engine = create_async_engine(f'sqlite+aiosqlite:///{DB_ADDRESS}')
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


def init_db(engine=sync_engine, drop_all=False):
    if drop_all:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        catboost_model = session.query(Models).filter_by(name='catboost').first()
        if catboost_model is None:
            default_model = Models(name='catboost', cost=500)
            session.add(default_model)
            session.commit()

        rf_model = session.query(Models).filter_by(name='random_forest').first()
        if rf_model is None:
            default_model = Models(name='random_forest', cost=250)
            session.add(default_model)
            session.commit()

        svc_model = session.query(Models).filter_by(name='svc').first()
        if svc_model is None:
            default_model = Models(name='svc', cost=100)
            session.add(default_model)
            session.commit()
