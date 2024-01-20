from backend.model.transaction import Transaction
from backend.repository.billing_repository import BillingRepository
from backend.schema.billing_schema import TransactionInfo
from backend.services.base_service import BaseService


class BillingService(BaseService):
    def __init__(self, billing_repository: BillingRepository):
        super().__init__(billing_repository)
        self.billing_repository = billing_repository

    def get_balance(self, user_id: int) -> int:
        return self.billing_repository.get_balance(user_id)

    def get_transaction_history(self, user_id: int) -> [TransactionInfo]:
        transactions = self.billing_repository.history(user_id)
        transaction_infos = [TransactionInfo(id=t.id, amount=t.amount, timestamp=t.created_at) for t in transactions]
        return transaction_infos

    def deposit(self, user_id: int, amount: int) -> TransactionInfo:
        transaction = self.billing_repository.deposit(user_id, amount)
        transaction_info = TransactionInfo(id=transaction.id, amount=transaction.amount,
                                           timestamp=transaction.created_at)
        return transaction_info

    def reserve_funds(self, user_id: int, amount: int) -> bool:
        current_balance, reserved_funds = self.billing_repository.get_balance_and_reserved_funds(user_id)
        available_balance = current_balance - reserved_funds
        if available_balance >= amount:
            self.billing_repository.create_reservation(user_id, amount)
            return True
        return False

    def finalize_transaction(self, user_id: int, amount: int) -> Transaction:
        transaction = self.billing_repository.finalize_reservation(user_id, amount)
        return transaction

    def cancel_reservation(self, user_id: int, amount: int) -> bool:
        return self.billing_repository.cancel_reservation(user_id, amount)

    def get_credits_report(self):
        report = self.billing_repository.get_credits_report()
        return report
