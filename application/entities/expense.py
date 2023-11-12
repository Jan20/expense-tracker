from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    expense_id: int
    timestamp: datetime
    description: str
    amount: float

    def __str__(self):
        return f"Timestamp: {self.timestamp}, description: {self.description}, Amount: {self.amount}"

    def __repr__(self):
        return str(self)
