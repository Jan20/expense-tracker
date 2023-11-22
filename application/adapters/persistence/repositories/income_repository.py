from typing import List
from sqlalchemy.orm import sessionmaker

from application.adapters.persistence.entities.entities import engine, IncomeEntity
from application.domain.entities.income import Income
from application.domain.ports.income_persistence_port import IncomePersistencePort


class IncomeRepository(IncomePersistencePort):
    Session = sessionmaker(bind=engine)

    def save(self, income: Income) -> Income:
        with self.Session() as session:
            session.add(
                IncomeEntity(
                    timestamp=income.date,
                    description=income.description,
                    amount=income.amount,
                )
            )
            session.commit()
            return income

    def get_all(self) -> List[Income]:
        with self.Session() as session:
            return [
                Income(
                    income_id=income_model.id,
                    date=income_model.timestamp,
                    description=income_model.description,
                    amount=income_model.amount
                )
                for income_model in session.query(IncomeEntity).all()
            ]

    def get_by_id(self, income_id: str) -> Income | None:
        with self.Session() as session:
            income_model = session.query(IncomeEntity).get(income_id)
            if income_model:
                return Income(
                    income_id=income_model.expense_id,
                    date=income_model.timestamp,
                    description=income_model.description,
                    amount=income_model.amount
                )

    def update(self, income: Income) -> None:
        with self.Session() as session:
            income_model = session.query(IncomeEntity).get(income.income_id)
            if income_model:
                income_model.expense_id = income.income_id
                income_model.timestamp = income.date
                income_model.description = income.description
                income_model.amount = income.amount
                session.commit()

    def delete(self, income_id: str) -> None:
        with self.Session() as session:
            income_model = IncomeEntity(id=income_id)
            session.delete(income_model)
            session.commit()

    def delete_all(self) -> None:
            with self.Session() as session:
                session.query(IncomeEntity).delete()
                session.commit()
