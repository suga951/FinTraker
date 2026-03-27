from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import TransactionType


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
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_dashboard_stats(db: Session, user_id: int, start_date: datetime | None = None, end_date: datetime | None = None):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    total_income = query.filter(Transaction.type == TransactionType.INCOME).with_entities(func.sum(Transaction.amount)).scalar() or 0.0
    total_expenses = query.filter(Transaction.type == TransactionType.EXPENSE).with_entities(func.sum(Transaction.amount)).scalar() or 0.0

    stats = query.with_entities(
        func.count(Transaction.tx_id),
        func.avg(Transaction.amount),
        func.min(Transaction.amount),
        func.max(Transaction.amount)
    ).first()

    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "net_balance": float(total_income) - float(total_expenses),
        "transaction_count": stats[0] or 0,
        "avg_amount": float(stats[1]) if stats[1] else 0.0,
        "min_amount": float(stats[2]) if stats[2] else None,
        "max_amount": float(stats[3]) if stats[3] else None,
        "by_category": {}
    }

