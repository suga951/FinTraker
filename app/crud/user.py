from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User


def get_by_email(db: Session, *, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create(db: Session, *, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(db: Session, *, email: str, password: str) -> User | None:
    user = get_by_email(db, email=email)
    if not User:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

