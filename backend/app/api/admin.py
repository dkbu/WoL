"""Admin-only endpoints. NOT YET ACCESS-CONTROLLED \u2014 lock this down before exposing publicly."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import users as db_users
from app.schemas.users import User

router = APIRouter()


@router.get("/admin/users")
def list_all_users(db: Session = Depends(get_db)) -> list[User]:
    """List every user and their id. Admin-only once access control exists."""
    return db_users.get_all_users(db)
