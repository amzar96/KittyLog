import logging

from sqlalchemy.orm import Session

from src.shared.models.user import User

logger = logging.getLogger(__name__)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(
        User.email == email,
        User.is_deleted == False,  # noqa: E712
    ).first()


def get_or_create_user(db: Session, userinfo: dict) -> User:
    user = get_user_by_email(db, userinfo["email"])
    if user:
        return user

    user = User(
        email=userinfo["email"],
        full_name=userinfo.get("name", ""),
        picture_url=userinfo.get("picture"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("created new user", extra={"email": user.email})
    return user
