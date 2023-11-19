from typing import List
from sqlalchemy.orm import sessionmaker

from application.adapters.persistence.entities.expense_entity import ExpenseEntity, engine
from application.domain.entities.expense import Expense
from application.domain.ports.expense_persistance_port import ExpensePersistencePort


class ExpenseRepository(ExpensePersistencePort):
    # Create a session
    Session = sessionmaker(bind=engine)

    def save(self, expense: Expense) -> None:
        session = self.Session()
        try:
            expense_model = ExpenseEntity(
                timestamp=expense.timestamp,
                description=expense.description,
                amount=expense.amount,
            )

            print(str(expense_model))

            session.add(expense_model)
            session.commit()
        finally:
            session.close()

    def get_all(self) -> List[Expense]:
        session = self.Session()

        # Define the format of the input string
        date_format = "%a, %d %b %Y %H:%M:%S %Z"

        try:
            expense_entities = session.query(ExpenseEntity).all()

            expenses = [
                Expense(
                    expense_id=expense_model.id,
                    timestamp=expense_model.timestamp,
                    description=expense_model.description,
                    amount=expense_model.amount
                )
                for expense_model in expense_entities
            ]
            return expenses
        finally:
            session.close()

    def get_by_id(self, expense_id: str) -> Expense | None:
        session = self.Session()
        try:
            expense_model = session.query(ExpenseEntity).filter_by(expense_id=expense_id).first()
            if expense_model:
                return Expense(
                    expense_id=expense_model.expense_id,
                    timestamp=expense_model.timestamp,
                    description=expense_model.description,
                    amount=expense_model.amount
                )
            return None
        finally:
            session.close()

    def update(self, expense: Expense) -> None:
        session = self.Session()
        try:
            expense_model = session.query(ExpenseEntity).filter_by(expense_id=expense.expense_id).first()
            if expense_model:
                expense_model.expense_id = expense.expense_id
                expense_model.timestamp = expense.timestamp
                expense_model.description = expense.description
                expense_model.amount = expense.amount
                session.commit()
        finally:
            session.close()

    def delete(self, expense: Expense) -> None:
        session = self.Session()
        try:
            expense_model = session.query(ExpenseEntity).filter_by(expense_id=expense.expense_id).first()
            if expense_model:
                session.delete(expense_model)
                session.commit()
        finally:
            session.close()

    def delete_all(self) -> None:
        session = self.Session()
        try:
            session.query(ExpenseEntity).delete()
            session.commit()

        finally:
            session.close()
