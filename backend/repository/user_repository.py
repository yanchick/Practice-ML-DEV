from contextlib import AbstractContextManager
from datetime import timedelta
from typing import Callable

from sqlalchemy.orm import Session

from backend.core.config import configs
from backend.model.user import User
from backend.repository.base_repository import BaseRepository
from backend.utils.date import get_now


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, User)

    def get_users_report(self):
        with self.session_factory() as session:
            active_since = get_now() - timedelta(minutes=configs.USER_ACTIVITY_INTERVAL)
            active_users_count = session.query(User).filter(User.last_activity_at >= active_since).count()
            return {"active_users": active_users_count}

    def read_by_email(self, email):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.email == email)
            user = query.first()
            return user

    def update_last_activity(self, user_id: int):
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.last_activity_at = get_now()
                session.commit()
