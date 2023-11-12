from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExpenseEntity(Base):
    __tablename__ = 'expenses'

    expense_id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    description = Column(String)
    amount = Column(Float)
