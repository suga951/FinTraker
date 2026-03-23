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
