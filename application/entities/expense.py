from datetime import datetime
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Expense:
    def __init__(self, user_id, amount, description, expense_id, timestamp):
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.expense_id = expense_id
        self.timestamp = timestamp

    def __str__(self):
        return f"Expense ID: {self.expense_id}, User ID: {self.user_id}, Amount: {self.amount}, Description: {self.description}, Timestamp: {self.timestamp}"

    def __repr__(self):
        return str(self)