from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class ExpenseModel(Base):
    __tablename__ = 'expenses'

    expense_id = Column(String, primary_key=True)
    user_id = Column(String)
    amount = Column(Float)
    description = Column(String)
    currency = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
