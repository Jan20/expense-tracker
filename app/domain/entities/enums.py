from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Period(Enum):
    YEARLY = "ye"
    MONTHLY = "me"
