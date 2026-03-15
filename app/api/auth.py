from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if crud.user.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code="409", detail="Email is already registered.")

    user = crud.user.create(db, email=user_in.email, password=user_in.password)
    return user
