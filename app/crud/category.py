from sqlalchemy.orm import Session
from app.models.category import Category, TransactionType
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Get system categories (user_id is None) and user categories
    return db.query(Category).filter(
        (Category.user_id == user_id) | (Category.user_id == None)
    ).offset(skip).limit(limit).all()


def create_category(db: Session, obj_in: CategoryCreate, user_id: int):
    db_obj = Category(
        name=obj_in.name,
        type=obj_in.type,
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_category(db: Session, db_obj: Category, obj_in: CategoryUpdate):
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_category(db: Session, category_id: int):
    db_obj = db.query(Category).get(category_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
