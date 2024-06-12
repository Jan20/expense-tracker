from datetime import datetime
from typing import List

from pandas import DataFrame, to_datetime

from app.adapters.persistence.repositories.transaction_repository import TransactionRepository
from app.domain.entities.enums import TransactionType, Period
from app.domain.entities.transaction import Transaction


class TransactionService:

    def __init__(self):
        self.transaction_repository = TransactionRepository()

    def get_transaction_dataframe(
        self,
        year: int,
        transaction_type: TransactionType,
    ) -> DataFrame:
        df = DataFrame(self.transaction_repository.get_all())
        df['date'] = to_datetime(df['date'])
        df = df[df['date'].dt.year == year]
        df = df[df['description'] != 'Investments']
        df = df[df['description'] != 'American Express']
        df = df[df['description'] != 'ZAHLUNG/ÜBERWEISUNG ERHALTEN BESTEN DANK']
        df = self.__filter_by_transaction_type(df, transaction_type)
        df = df.drop(columns=['transaction_id'])
        return df

    @staticmethod
    def __filter_by_transaction_type(df: DataFrame, transaction_type: TransactionType):
        if transaction_type is TransactionType.INCOME:
            return df[df['amount'] >= 0]
        if transaction_type is TransactionType.EXPENSE:
            return df[df['amount'] < 0]

    @staticmethod
    def __filter_by_period(df: DataFrame, period: Period):
        if period is Period.YEARLY:
            return df[df['amount'] >= 0]
        if period is TransactionType.EXPENSE:
            return df[df['amount'] < 0]

    def create_transaction(self, date: datetime, description: str, amount: float) -> Transaction:
        transaction = Transaction(
            transaction_id=None,
            date=date,
            description=description,
            amount=amount
        )
        return self.transaction_repository.save(transaction)

    def get_transactions(self) -> List[Transaction]:
        return self.transaction_repository.get_all()

    def get_transaction(self, transaction_id: str) -> Transaction:
        expense = self.transaction_repository.get_by_id(transaction_id)
        if not expense:
            raise ValueError("Expense not found")
        return expense

    def update_transaction(self, transaction_id: str, date: datetime, description: str, amount: float) -> Transaction:
        expense = self.get_transaction(transaction_id)

        if expense is None:
            raise ValueError(f"Expense with ID {transaction_id} not found.")

        expense.date = date
        expense.description = description
        expense.amount = amount

        self.transaction_repository.update(expense)

        return expense

    def delete_transaction(self, transaction_id: str):
        self.transaction_repository.delete(transaction_id)

    def delete_transactions(self):
        self.transaction_repository.delete_all()
