from datetime import datetime

from application.adapters.persistence.repositories.expense_repository import ExpenseRepository
from application.entities.expense import Expense
from application.use_cases.expense_usecase import ExpenseUseCase


class ExpenseService(ExpenseUseCase):
    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repository = expense_repository

    def create_expense(self, timestamp: datetime, description: str, amount: float) -> Expense:

        expense = Expense(timestamp=timestamp, description=description, amount=amount)

        self.expense_repository.save(expense)

        return expense

    def get_expense(self, expense_id: str) -> Expense:
        expense = self.expense_repository.get_by_id(expense_id)
        if not expense:
            raise ValueError("Expense not found")
        return expense

    def update_expense(self, expense_id: str, timestamp: datetime, description: str, amount: float) -> Expense:
        expense = self.get_expense(expense_id)

        if expense is None:
            raise ValueError(f"Expense with ID {expense_id} not found.")

        expense.timestamp = timestamp
        expense.description = description
        expense.amount = amount

        self.expense_repository.update(expense)

        return expense

    def delete_expense(self, expense_id: str):
        expense = self.get_expense(expense_id)
        self.expense_repository.delete(expense)

        # Optionally, you can perform cleanup or other actions here

        return
