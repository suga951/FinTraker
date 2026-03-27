from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, categories, transactions, dashboard
from app.core.config import settings

app = FastAPI(
    title="FinTrakr API",
    description="Personal Expense Tracker API with budgets and alerts.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to FinTrakr API!"}


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)
