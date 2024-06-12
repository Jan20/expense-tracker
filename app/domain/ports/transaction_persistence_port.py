from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.transaction import Transaction


class TransactionPersistencePort(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        """Save an expense entity to the data storage."""
        pass

    @abstractmethod
    def get_all(self) -> List[Transaction]:
        """Retrieve all expenses from the data storage."""
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: str) -> Transaction | None:
        """Retrieve an expense by its ID from the data storage."""
        pass

    @abstractmethod
    def update(self, transaction: Transaction) -> None:
        """Update an existing expense entity in the data storage."""
        pass

    @abstractmethod
    def delete(self, transaction_id: str) -> None:
        """Delete an expense entity from the data storage."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all stored expenses"""
        pass
