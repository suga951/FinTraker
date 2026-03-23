from pydantic import BaseModel, Field
from app.models.category import TransactionType


class CategoryBase(BaseModel):
    name: str = Field(..., description="Category name.")
    type: TransactionType = Field(..., description="Category type (income or expense).")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: TransactionType | None = None


class Category(CategoryBase):
    id: int
    user_id: int | None = None

    model_config = {"from_attributes": True}
