from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.category import Category, TransactionType


def seed_default_categories():
    db: Session = SessionLocal()
    try:
        # Default Categories
        default_categories = [
            # Income
            ("Salary", TransactionType.INCOME),
            ("Business", TransactionType.INCOME),
            ("Gifts", TransactionType.INCOME),
            ("Extra Income", TransactionType.INCOME),
            
            # Expense
            ("Food", TransactionType.EXPENSE),
            ("Transport", TransactionType.EXPENSE),
            ("Rent", TransactionType.EXPENSE),
            ("Shopping", TransactionType.EXPENSE),
            ("Utilities", TransactionType.EXPENSE),
            ("Entertainment", TransactionType.EXPENSE),
            ("Health", TransactionType.EXPENSE),
            ("Insurance", TransactionType.EXPENSE),
            ("Others", TransactionType.EXPENSE),
        ]

        for name, type_ in default_categories:
            # Check if category already exists as a system category
            exists = db.query(Category).filter(
                Category.name == name,
                Category.type == type_,
                Category.user_id == None
            ).first()
            
            if not exists:
                db_category = Category(name=name, type=type_, user_id=None)
                db.add(db_category)
                print(f"Adding system category: {name} ({type_})")
        
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    print("Seedling default categories...")
    seed_default_categories()
    print("Seeding complete.")
