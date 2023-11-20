from datetime import datetime
from typing import List

from application.adapters.persistence.repositories.expense_repository import ExpenseRepository
from application.domain.entities.expense import Expense
from application.use_cases.expense_usecase import ExpenseUseCase


class ExpenseService(ExpenseUseCase):

    def __init__(self):
        self.expense_repository = ExpenseRepository()

    def create_expense(self, date: datetime, description: str, amount: float) -> Expense:

        expense = Expense(expense_id=None, date=date, description=description, amount=amount)

        self.expense_repository.save(expense)

        return expense

    def get_expenses(self) -> List[Expense]:
        expenses: List[Expense] = self.expense_repository.get_all()

        if not expenses:
            raise ValueError("Expense not found")
        return expenses

    def get_expense(self, expense_id: str) -> Expense:
        expense = self.expense_repository.get_by_id(expense_id)
        if not expense:
            raise ValueError("Expense not found")
        return expense

    def update_expense(self, expense_id: str, date: datetime, description: str, amount: float) -> Expense:
        expense = self.get_expense(expense_id)

        if expense is None:
            raise ValueError(f"Expense with ID {expense_id} not found.")

        expense.date = date
        expense.description = description
        expense.amount = amount

        self.expense_repository.update(expense)

        return expense

    def delete_expense(self, expense_id: str):
        expense = self.get_expense(expense_id)
        self.expense_repository.delete(expense)

    def delete_expenses(self):
        """ Deletes all expenses."""
        self.expense_repository.delete_all()
