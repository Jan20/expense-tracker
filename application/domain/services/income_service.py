from datetime import datetime
from typing import List

from application.adapters.persistence.repositories.income_repository import IncomeRepository
from application.domain.entities.income import Income
from application.use_cases.income_usecase import IncomeUseCase


class IncomeService(IncomeUseCase):

    def __init__(self):
        self.income_repository = IncomeRepository()

    def create_income(self, date: datetime, description: str, amount: float) -> Income:
        return self.income_repository.save(
            Income(
                income_id=None,
                date=date,
                description=description,
                amount=amount
            )
        )

    def get_incomes(self) -> List[Income]:
        return self.income_repository.get_all()

    def get_income(self, income_id: str) -> Income:
        income = self.income_repository.get_by_id(income_id)
        if not income:
            raise ValueError("Income not found")
        return income

    def update_income(self, income_id: str, date: datetime, description: str, amount: float) -> Income:
        expense = self.get_income(income_id)

        if expense is None:
            raise ValueError(f"Income with ID {income_id} not found.")

        expense.date = date
        expense.description = description
        expense.amount = amount

        self.income_repository.update(expense)

        return expense

    def delete_income(self, income_id: str):
        self.income_repository.delete(income_id)

    def delete_incomes(self):
        self.income_repository.delete_all()
