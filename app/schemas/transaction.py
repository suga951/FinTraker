from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from app.models.category import TransactionType


class TransactionBase(BaseModel):
    description: str = Field(..., description="Transaction description.")
    amount: Decimal = Field(..., description="Transaction amount.")
    type: TransactionType = Field(..., description="Transaction type (income or expense).")
    category_id: int = Field(..., description="Category ID.")
    date: datetime = Field(default_factory=datetime.utcnow, description="Transaction date.")


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    description: str | None = None
    amount: Decimal | None = None
    type: TransactionType | None = None
    category_id: int | None = None
    date: datetime | None = None


class Transaction(TransactionBase):
    tx_id: int
    user_id: int

    model_config = {"from_attributes": True}
