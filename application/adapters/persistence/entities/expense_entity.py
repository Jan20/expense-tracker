from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine, exc
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

# Construct the database URL for SQLAlchemy
database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"

engine = create_engine(url=database_url)

Base = declarative_base()
Base.metadata.bind = engine


class ExpenseEntity(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(type_=DateTime)
    description = Column(type_=String)
    amount = Column(type_=Float)


try:
    # Attempt to create all tables defined in the entities
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

except exc.SQLAlchemyError as e:
    # Handle SQLAlchemy-specific exceptions
    print(f"Have you started Docker?🔥🤔 \n {e}")

except Exception as e:
    # Handle other exceptions
    print(f"Unexpected error occurred: {e}")
