from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.api import deps
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new category for the current user.
    """
    return crud.category.create_category(db, obj_in=category_in, user_id=current_user.id)


@router.get("/", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retrieve all categories available to the current user (system and personal).
    """
    return crud.category.get_categories(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get a specific category by ID.
    """
    category = crud.category.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id is not None and category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return category


@router.put("/{category_id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: CategoryUpdate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update a category.
    """
    category = crud.category.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id is None:
        raise HTTPException(status_code=403, detail="System categories cannot be updated")
    if category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.category.update_category(db, db_obj=category, obj_in=category_in)


@router.delete("/{category_id}", response_model=Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete a category.
    """
    category = crud.category.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id is None:
        raise HTTPException(status_code=403, detail="System categories cannot be deleted")
    if category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.category.delete_category(db, category_id=category_id)
