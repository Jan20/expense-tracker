from abc import ABC, abstractmethod

from application.entities.expense import Expense


class ExpensePersistencePort(ABC):
    @abstractmethod
    def save(self, expense: Expense) -> None:
        """Save an expense entity to the data storage."""
        pass

    @abstractmethod
    def get_by_id(self, expense_id: str) -> Expense:
        """Retrieve an expense by its ID from the data storage."""
        pass

    @abstractmethod
    def update(self, expense: Expense) -> None:
        """Update an existing expense entity in the data storage."""
        pass

    @abstractmethod
    def delete(self, expense: Expense) -> None:
        """Delete an expense entity from the data storage."""
        pass
