from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from model.user import User, Transaction, Model


from repository.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    def get_session(self) -> Session:
        """
        Get a new session from the session factory.
        """
        return self.session_factory().__enter__()

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

    def commit(self):
        pass

    def choose_model(self, user: User, model_id: int):
        # Use self.get_session().query here
        model = self.get_session().query(Model).filter(Model.id == model_id).first()
        if not model:
            raise ValidationError(detail=f"Model with id {model_id} does not exist")

        # Update the user's chosen model
        user.chosen_model_id = model_id

        try:
            # Commit the user update to the database
            self.commit()
        except Exception as e:
            # Handle any errors that occur during the commit
            raise ValidationError(detail="Failed to choose the model") from e
