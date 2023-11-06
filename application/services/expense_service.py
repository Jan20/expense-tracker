from application.entities.expense import Expense
from application.use_cases.expense_usecase import ExpenseUseCase


class ExpenseService(ExpenseUseCase):
    def __init__(self, expense_repository: ExpenseRepository, email_service: EmailService):
        self.expense_repository = expense_repository
        self.email_service = email_service

    def create_expense(self, user_id: str, amount: float, description: str, currency_code: str) -> Expense:
        # Validate and create a new expense entity
        currency = Currency(currency_code)
        if not currency.is_valid():
            raise ValueError("Invalid currency code")

        expense = Expense(user_id, amount, description, currency)

        # Save the expense to the repository
        self.expense_repository.save(expense)

        # Optionally, you can notify the user about the expense
        self.email_service.send_expense_notification(user_id, expense)

        return expense

    def get_expense(self, expense_id: str) -> Expense:
        expense = self.expense_repository.get_by_id(expense_id)
        if not expense:
            raise ValueError("Expense not found")
        return expense

    def update_expense(self, expense_id: str, amount: float, description: str, currency_code: str) -> Expense:
        expense = self.get_expense(expense_id)
        currency = Currency(currency_code)
        if not currency.is_valid():
            raise ValueError("Invalid currency code")

        expense.amount = amount
        expense.description = description
        expense.currency = currency

        self.expense_repository.update(expense)

        return expense

    def delete_expense(self, expense_id: str):
        expense = self.get_expense(expense_id)
        self.expense_repository.delete(expense)

        # Optionally, you can perform cleanup or other actions here

        return
