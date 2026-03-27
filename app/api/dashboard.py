from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.user import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_current_month_range():
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end


@router.get("/", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(deps.get_db),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    all_time: bool = Query(False, description="Get all-time stats instead of current month"),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get dashboard stats for the current user.
    Defaults to current month if no date range is provided.
    Use all_time=true to get all-time statistics.
    """
    if all_time:
        start_date = None
        end_date = None
    elif not start_date or not end_date:
        start_date, end_date = get_current_month_range()

    return crud.user.get_dashboard_stats(db, user_id=current_user.id, start_date=start_date, end_date=end_date)