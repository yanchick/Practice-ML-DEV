# core/database.py

from sqlalchemy.orm import Session
from contextlib import AbstractContextManager, contextmanager
from sqlalchemy import create_engine, orm

from core.config import configs
from model.base_model import BaseModel
from model.base_model import Model, Transaction # Import BaseModel first
from model.user import User
  # Now import the other models

@contextmanager
def get_db() -> AbstractContextManager[Session]:
    db = Database(configs.DATABASE_URI)
    try:
        yield db
    finally:
        db.close()

class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        User.metadata.create_all(self._engine)
        Transaction.metadata.create_all(self._engine)
        Model.metadata.create_all(self._engine)


    @contextmanager
    def session(self) -> AbstractContextManager[Session]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def init_db():
    # Create an instance of the Database class
    db = Database(configs.DATABASE_URI)

    # Create the database tables
    db.create_database()

    # Optionally, add additional initialization logic here

#if __name__ == "__main__":
    # Run init_db when this script is executed directly
    #init_db()
# core/database.py

# ... (previous code)

@contextmanager
def get_session() -> AbstractContextManager[Session]:
    db = Database(configs.DATABASE_URI)
    try:
        yield db
    finally:
        db.close()

# ... (remaining code)
