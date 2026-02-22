from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.shared.models.user import User
from src.utils.db import get_db


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_info = request.session.get("user")
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    user = db.query(User).filter(
        User.email == user_info["email"],
        User.is_deleted == False,  # noqa: E712
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
