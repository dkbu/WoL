"""Admin-only endpoints, restricted to admins."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import users as db_users
from app.deps import require_admin
from app.schemas.users import User, UserRoleUpdate

router = APIRouter()


@router.get("/admin/users")
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[User]:
    """List every user and their id. Admin-only."""
    return db_users.get_all_users(db)


@router.patch("/admin/users/{user_id}/roles")
def update_user_roles(
    user_id: uuid.UUID,
    roles: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> User:
    """Grant or revoke curator/admin status for a user. Admin-only."""
    result = db_users.set_user_roles(
        db, user_id, is_curator=roles.is_curator, is_admin=roles.is_admin
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return result
