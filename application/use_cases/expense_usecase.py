from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from application.domain.entities.expense import Expense


class ExpenseUseCase(ABC):
    @abstractmethod
    def create_expense(self, timestamp: datetime, description: str, amount: float) -> Expense:
        """Create a new expense and return the created expense entity."""
        pass

    @abstractmethod
    def get_expenses(self) -> List[Expense]:
        """Retrieve all expenses and return the corresponding expense entities."""
        pass

    @abstractmethod
    def get_expense(self, expense_id: str) -> Expense:
        """Retrieve an expense by its ID and return the corresponding expense entity."""
        pass

    @abstractmethod
    def update_expense(self, expense_id: str, timestamp: datetime, description: str, amount: float) -> Expense:
        """Update an existing expense and return the updated expense entity."""
        pass

    @abstractmethod
    def delete_expense(self, expense_id: str):
        """Delete an expense by its ID."""
        pass

    @abstractmethod
    def delete_expenses(self):
        """Deletes all expenses."""
        pass
