from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from model.user import User
from model.base_model import Transaction

from repository.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    def get_session(self) -> AbstractContextManager[Session]:
        """
        Get a new session from the session factory.
        """
        return self.session_factory()

    def create(self, user: User) -> User:
        """
        Create a new user in the database.
        """
        with self.get_session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)  # Refresh the user object to get the updated values from the database
        return user
    def get_user_transaction_history(self, user_id: int) -> List[Transaction]:
        """
        Get the transaction history for a user.
        """
        with self.get_session() as session:
            user = session.query(User).get(user_id)
            if not user:
                return []  # Return an empty list if the user is not found

            # Assuming you have a relationship between User and Transaction models
            return user.transactions

