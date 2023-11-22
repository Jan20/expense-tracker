from abc import ABC, abstractmethod
from typing import List

from application.domain.entities.expense import Expense


class ExpensePersistencePort(ABC):
    @abstractmethod
    def save(self, expense: Expense) -> Expense:
        """Save an expense entity to the data storage."""
        pass

    @abstractmethod
    def get_all(self) -> List[Expense]:
        """Retrieve all expenses from the data storage."""
        pass

    @abstractmethod
    def get_by_id(self, expense_id: str) -> Expense | None:
        """Retrieve an expense by its ID from the data storage."""
        pass

    @abstractmethod
    def update(self, expense: Expense) -> None:
        """Update an existing expense entity in the data storage."""
        pass

    @abstractmethod
    def delete(self, expense_id: str) -> None:
        """Delete an expense entity from the data storage."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all stored expenses"""
        pass
