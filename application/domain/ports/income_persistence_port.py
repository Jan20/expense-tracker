from abc import ABC, abstractmethod
from typing import List

from application.domain.entities.income import Income


class IncomePersistencePort(ABC):
    @abstractmethod
    def save(self, income: Income) -> Income:
        """Save an income entity to the data storage."""
        pass

    @abstractmethod
    def get_all(self) -> List[Income]:
        """Retrieve all incomes from the data storage."""
        pass

    @abstractmethod
    def get_by_id(self, income_id: str) -> Income | None:
        """Retrieve an income by its ID from the data storage."""
        pass

    @abstractmethod
    def update(self, income: Income) -> None:
        """Update an existing income entity in the data storage."""
        pass

    @abstractmethod
    def delete(self, income_id: str) -> None:
        """Delete an income entity from the data storage."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all stored incomes"""
        pass
