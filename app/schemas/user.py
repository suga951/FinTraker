from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email.")

class UserCreate(UserBase):
    password: str = Field(..., description="User's password.")

class UserOut(UserBase):
    id: int
    is_active: bool
    
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenData(BaseModel):
    email: str | None = None


class DashboardStats(BaseModel):
    total_income: float = 0.0
    total_expenses: float = 0.0
    net_balance: float = 0.0
    transaction_count: int = 0
    avg_amount: float = 0.0
    min_amount: float | None = None
    max_amount: float | None = None
    by_category: dict = {}

    model_config = {"from_attributes": True}
