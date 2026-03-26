from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.api import deps
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.models.user import User

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: TransactionCreate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new transaction for the current user.
    """
    # Verify category exists and belongs to user or is system
    category = crud.category.get_category(db, category_id=transaction_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id is not None and category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot use another user's category")
        
    return crud.transaction.create_transaction(db, obj_in=transaction_in, user_id=current_user.id)


@router.get("/", response_model=List[Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retrieve all transactions for the current user.
    """
    return crud.transaction.get_transactions(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{tx_id}", response_model=Transaction)
def read_transaction(
    *,
    db: Session = Depends(deps.get_db),
    tx_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get a specific transaction by ID.
    """
    transaction = crud.transaction.get_transaction(db, tx_id=tx_id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{tx_id}", response_model=Transaction)
def update_transaction(
    *,
    db: Session = Depends(deps.get_db),
    tx_id: int,
    transaction_in: TransactionUpdate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update a transaction.
    """
    transaction = crud.transaction.get_transaction(db, tx_id=tx_id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    if transaction_in.category_id is not None:
        category = crud.category.get_category(db, category_id=transaction_in.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        if category.user_id is not None and category.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Cannot use another user's category")

    return crud.transaction.update_transaction(db, db_obj=transaction, obj_in=transaction_in)


@router.delete("/{tx_id}", response_model=Transaction)
def delete_transaction(
    *,
    db: Session = Depends(deps.get_db),
    tx_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete a transaction.
    """
    transaction = crud.transaction.get_transaction(db, tx_id=tx_id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return crud.transaction.delete_transaction(db, tx_id=tx_id)
