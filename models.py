from sqlalchemy import Column, Integer, Float, String, Date
from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    amount = Column(Float)
    date = Column(Date)
    transaction_type = Column(String)
