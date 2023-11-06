from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.persistence.models.expense_model import ExpenseModel
from application.entities.expense import Expense
from application.ports.expense_persistance_port import ExpensePersistencePort


class ExpenseRepository(ExpensePersistencePort):
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def save(self, expense: Expense) -> None:
        session = self.Session()
        try:
            expense_model = ExpenseModel(
                expense_id=expense.expense_id,
                user_id=expense.user_id,
                amount=expense.amount,
                description=expense.description,
            )
            session.add(expense_model)
            session.commit()
        finally:
            session.close()

    def get_by_id(self, expense_id: str) -> Expense:
        session = self.Session()
        try:
            expense_model = session.query(ExpenseModel).filter_by(expense_id=expense_id).first()
            if expense_model:
                return Expense(
                    user_id=expense_model.user_id,
                    amount=expense_model.amount,
                    description=expense_model.description,
                    expense_id=expense_model.expense_id,
                    timestamp=expense_model.timestamp,
                )
            return None
        finally:
            session.close()

    def update(self, expense: Expense) -> None:
        session = self.Session()
        try:
            expense_model = session.query(ExpenseModel).filter_by(expense_id=expense.expense_id).first()
            if expense_model:
                expense_model.user_id = expense.user_id
                expense_model.amount = expense.amount
                expense_model.description = expense.description
                session.commit()
        finally:
            session.close()

    def delete(self, expense: Expense) -> None:
        session = self.Session()
        try:
            expense_model = session.query(ExpenseModel).filter_by(expense_id=expense.expense_id).first()
            if expense_model:
                session.delete(expense_model)
                session.commit()
        finally:
            session.close()
