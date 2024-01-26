# repository/model_repository.py
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from model.user import Model
from repository.base_repository import BaseRepository

class ModelRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Model)


    def get_session(self) -> Session:
        """
        Get a new session from the session factory.
        """
        return self.session_factory().__enter__()


    def get_model_by_id(self, modelid: int):
        with self.get_session() as session:
            return session.query(Model).filter(Model.id == modelid).first()

    def get_all_models(self):
        with self.get_session() as session:
            return session.query(Model).all()
