from sqlalchemy import func, desc
from sqlalchemy.exc import NoResultFound

from backend.core.exceptions import NotFoundError
from backend.model.transaction import Transaction
from backend.model.user import User
from backend.repository.base_repository import BaseRepository


class BillingRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory, Transaction)

    def get_balance(self, user_id: int):
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return user.balance
            else:
                raise NotFoundError(f"User with id {user_id} not found")

    def get_balance_and_reserved_funds(self, user_id: int):
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return user.balance, user.reserved_funds
            else:
                raise NotFoundError(f"User with id {user_id} not found")

    def deposit(self, user_id: int, amount: int) -> Transaction:
        with self.session_factory() as session:
            try:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    transaction = Transaction(user_id=user_id, amount=amount)
                    session.add(transaction)
                    user.balance += amount
                    session.commit()
                    new_transaction = session.query(Transaction).get(transaction.id)
                    return new_transaction
                else:
                    raise NotFoundError(f"User with id {user_id} not found")
            except Exception as e:
                session.rollback()
                raise e

    def history(self, user_id: int):
        with self.session_factory() as session:
            transactions = session.query(Transaction) \
                .filter(Transaction.user_id == user_id) \
                .order_by(desc(Transaction.created_at)) \
                .all()
            return transactions

    def get_credits_report(self):
        with self.session_factory() as session:
            total_credits_purchased = session.query(
                func.coalesce(func.sum(Transaction.amount), 0)
            ).filter(Transaction.amount > 0).scalar()

            total_credits_spent = session.query(
                func.coalesce(func.sum(Transaction.amount), 0)
            ).filter(Transaction.amount < 0).scalar()

            return {
                "total_credits_purchased": total_credits_purchased,
                "total_credits_spent": abs(total_credits_spent)
            }

    def create_reservation(self, user_id: int, amount: int) -> bool:
        with self.session_factory() as session:
            try:
                user = session.query(User).filter(User.id == user_id).one()
                user.reserved_funds += amount
                session.commit()
                return True
            except NoResultFound:
                raise NotFoundError(f"User with id {user_id} not found")

    def cancel_reservation(self, user_id: int, amount: int) -> bool:
        with self.session_factory() as session:
            try:
                user = session.query(User).filter(User.id == user_id).one()
                user.reserved_funds -= amount
                session.commit()
                return True
            except NoResultFound:
                raise NotFoundError(f"User with id {user_id} not found")

    def finalize_reservation(self, user_id: int, amount: int) -> Transaction:
        with self.session_factory() as session:
            try:
                user = session.query(User).filter(User.id == user_id).one()
                if user.reserved_funds >= amount:
                    user.reserved_funds -= amount
                    user.balance -= amount
                    transaction = Transaction(user_id=user_id, amount=-amount)
                    session.add(transaction)
                    session.commit()
                    new_transaction = session.query(Transaction).get(transaction.id)
                    return new_transaction
                else:
                    raise ValueError("Insufficient reserved funds")
            except NoResultFound:
                raise NotFoundError(f"User with id {user_id} not found")
