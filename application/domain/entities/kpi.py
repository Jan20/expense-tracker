from dataclasses import dataclass
from typing import Optional


@dataclass
class KPI:
    total_income: Optional[float]
    total_expenses: Optional[float]
    total_savings: Optional[float]
    savings_rate: Optional[float]

    def __str__(self):
        return (f"income: {self.total_income}, "
                f"expenses: {self.total_expenses}, "
                f"total_savings: {self.total_savings}, "
                f"savings_rate: {self.savings_rate}")

    def __repr__(self):
        return str(self)
