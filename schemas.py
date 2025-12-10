from pydantic import BaseModel, ConfigDict
from datetime import date


class TransactionBase(BaseModel):
    name: str
    category: str
    amount: float
    date: date
    transaction_type: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
