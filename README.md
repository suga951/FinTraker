# FinTrakr

Personal Expense Tracker API with budgets and alerts.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose

## Setup

1. **Clone the repository**

2. **Configure environment variables**
   
   Copy `.env.example` to `.env` and adjust values if needed:
   ```bash
   cp .env.example .env
   ```

3. **Start PostgreSQL**
   ```bash
   docker-compose up -d
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

5. **Activate virtual environment**
   ```bash
   # Linux/Mac
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

6. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Run

1. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

2. **Seed initial categories (optional)**
   ```bash
   python app/seed_categories.py
   ```

3. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
