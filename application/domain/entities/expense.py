from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    expense_id: Optional[str]
    timestamp: datetime
    description: str
    amount: float

    def __str__(self):
        return f"Timestamp: {self.timestamp}, description: {self.description}, Amount: {self.amount}"

    def __repr__(self):
        return str(self)
