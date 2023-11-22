from typing import List
from sqlalchemy.orm import sessionmaker

from application.adapters.persistence.entities.entities import ExpenseEntity, engine
from application.domain.entities.expense import Expense
from application.domain.ports.expense_persistence_port import ExpensePersistencePort


class ExpenseRepository(ExpensePersistencePort):
    Session = sessionmaker(bind=engine)

    def save(self, expense: Expense) -> Expense:
        with self.Session() as session:
            session.add(
                ExpenseEntity(
                    timestamp=expense.date,
                    description=expense.description,
                    amount=expense.amount,
                )
            )
            session.commit()
            return expense

    def get_all(self) -> List[Expense]:
        with self.Session() as session:
            return [
                Expense(
                    expense_id=expense_model.id,
                    date=expense_model.timestamp,
                    description=expense_model.description,
                    amount=expense_model.amount
                )
                for expense_model in session.query(ExpenseEntity).all()
            ]

    def get_by_id(self, expense_id: str) -> Expense | None:
        with self.Session() as session:
            expense_model = session.query(ExpenseEntity).get(expense_id)
            if expense_model:
                return Expense(
                    expense_id=expense_model.expense_id,
                    date=expense_model.timestamp,
                    description=expense_model.description,
                    amount=expense_model.amount
                )

    def update(self, expense: Expense) -> None:
        with self.Session() as session:
            expense_model = session.query(ExpenseEntity).get(expense.expense_id)
            if expense_model:
                expense_model.expense_id = expense.expense_id
                expense_model.timestamp = expense.date
                expense_model.description = expense.description
                expense_model.amount = expense.amount
                session.commit()

    def delete(self, expense_id: str) -> None:
        with self.Session() as session:
            expense_model = ExpenseEntity(id=expense_id)
            session.delete(expense_model)
            session.commit()

    def delete_all(self) -> None:
        with self.Session() as session:
            session.query(ExpenseEntity).delete()
            session.commit()
