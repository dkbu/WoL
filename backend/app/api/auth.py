from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.db import users as db_users
from app.deps import COOKIE_NAME, get_current_user
from app.schemas.auth import LoginRequest
from app.schemas.users import User
from app.security import create_access_token

router = APIRouter()


@router.post("/auth/login")
def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> User:
    user = db_users.authenticate_user(db, credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    token = create_access_token(user.id)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return user


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    response.delete_cookie(COOKIE_NAME)


@router.get("/auth/me")
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
