from fastapi import FastAPI

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
