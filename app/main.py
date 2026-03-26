from fastapi import FastAPI

from app.api import auth, categories, transactions

app = FastAPI(
    title="FinTrakr API",
    description="Personal Expense Tracker API with budgets and alerts.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to FinTrakr API!"}


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
