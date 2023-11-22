from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from application.domain.entities.income import Income


class IncomeUseCase(ABC):
    @abstractmethod
    def create_income(self, timestamp: datetime, description: str, amount: float) -> Income:
        """Create a new income object and return the created income entity."""
        pass

    @abstractmethod
    def get_incomes(self) -> List[Income]:
        """Retrieve all expenses and return the corresponding expense entities."""
        pass

    @abstractmethod
    def get_income(self, income_id: str) -> Income:
        """Retrieve an expense by its ID and return the corresponding expense entity."""
        pass

    @abstractmethod
    def update_income(self, income_id: str, timestamp: datetime, description: str, amount: float) -> Income:
        """Update an existing expense and return the updated expense entity."""
        pass

    @abstractmethod
    def delete_income(self, income_id: str):
        """Delete an expense by its ID."""
        pass

    @abstractmethod
    def delete_incomes(self):
        """Deletes all expenses."""
        pass
