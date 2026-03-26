from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def get_transaction(db: Session, tx_id: int, user_id: int):
    return db.query(Transaction).filter(
        Transaction.tx_id == tx_id, Transaction.user_id == user_id
    ).first()


def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).offset(skip).limit(limit).all()


def create_transaction(db: Session, obj_in: TransactionCreate, user_id: int):
    db_obj = Transaction(
        **obj_in.model_dump(),
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_transaction(db: Session, db_obj: Transaction, obj_in: TransactionUpdate):
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_transaction(db: Session, tx_id: int):
    db_obj = db.query(Transaction).get(tx_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
