from dataclasses import dataclass
from typing import Optional


@dataclass
class KPI:
    income: Optional[float]
    expenses: Optional[float]
    savings: Optional[float]

    def calculate_savings_rate(self):
        if self.income == 0:
            return 0
        return (self.savings / self.income) * 100

    def __str__(self):
        return f"income: {self.income}, expenses: {self.expenses}, savings: {self.savings}"

    def __repr__(self):
        return str(self)
