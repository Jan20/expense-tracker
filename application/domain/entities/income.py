from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Income:
    income_id: Optional[str]
    date: datetime
    description: str
    amount: float

    def __str__(self):
        return f"Timestamp: {self.date}, description: {self.description}, Amount: {self.amount}"

    def __repr__(self):
        return str(self)
