from pydantic import BaseModel, Field
from app.models.category import TransactionType


class CategoryBase(BaseModel):
    name: str = Field(..., description="Category name.")
    type: TransactionType = Field(..., description="Category type (income or expense).")
    color: str | None = Field(None, description="Hex color code (e.g., #FF5733).")
    emoji: str | None = Field(None, description="Emoji icon (e.g., 🛒).")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: TransactionType | None = None
    color: str | None = None
    emoji: str | None = None


class Category(CategoryBase):
    id: int
    user_id: int | None = None

    model_config = {"from_attributes": True}
