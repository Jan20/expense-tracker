import logging
from typing import List
from sqlalchemy.orm import sessionmaker

from app.adapters.persistence.entities.entities import TransactionEntity, engine
from app.domain.entities.transaction import Transaction
from app.domain.ports.transaction_persistence_port import TransactionPersistencePort

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionRepository(TransactionPersistencePort):
    Session = sessionmaker(bind=engine)

    def save(self, transaction: Transaction) -> Transaction:
        try:
            with self.Session() as session:
                expense_entity = TransactionEntity(
                    timestamp=transaction.date,
                    description=transaction.description,
                    amount=transaction.amount,
                )
                session.add(expense_entity)
                logger.info(f"Transaction saved: {transaction}")
                session.commit()
                return transaction

        except Exception as e:
            logger.error(f"Error saving transaction: {e}")
            raise

    def get_all(self) -> List[Transaction]:
        with self.Session() as session:
            return [
                Transaction(
                    transaction_id=expense_model.id,
                    date=expense_model.timestamp,
                    description=expense_model.description,
                    amount=expense_model.amount
                )
                for expense_model in session.query(TransactionEntity).all()
            ]

    def get_by_id(self, transaction_id: str) -> Transaction | None:
        with self.Session() as session:
            expense_model = session.query(TransactionEntity).get(transaction_id)
            if expense_model:
                return Transaction(
                    transaction_id=expense_model.expense_id,
                    date=expense_model.timestamp,
                    description=expense_model.description,
                    amount=expense_model.amount
                )

    def update(self, transaction: Transaction) -> None:
        with self.Session() as session:
            expense_model = session.query(TransactionEntity).get(transaction.transaction_id)
            if expense_model:
                expense_model.expense_id = transaction.transaction_id
                expense_model.timestamp = transaction.date
                expense_model.description = transaction.description
                expense_model.amount = transaction.amount
                session.commit()

    def delete(self, transaction_id: str) -> None:
        with self.Session() as session:
            expense_model = TransactionEntity(id=transaction_id)
            session.delete(expense_model)
            session.commit()

    def delete_all(self) -> None:
        with self.Session() as session:
            session.query(TransactionEntity).delete()
            session.commit()
