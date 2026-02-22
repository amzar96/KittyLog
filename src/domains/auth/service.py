import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.shared.models.rbac import Role, UserRole
from src.shared.models.subscription import Plan, UserSubscription
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
        _ensure_role_and_plan(db, user)
        return user

    user = User(
        email=userinfo["email"],
        full_name=userinfo.get("name", ""),
        picture_url=userinfo.get("picture"),
    )
    db.add(user)
    db.flush()

    _assign_default_role(db, user)
    _assign_free_plan(db, user)

    db.commit()
    db.refresh(user)
    logger.info("created new user", extra={"email": user.email})
    return user


def _ensure_role_and_plan(db: Session, user: User) -> None:
    has_role = db.query(UserRole).filter(
        UserRole.user_id == user.id,
        UserRole.is_deleted == False,  # noqa: E712
    ).first()

    has_sub = db.query(UserSubscription).filter(
        UserSubscription.user_id == user.id,
        UserSubscription.is_deleted == False,  # noqa: E712
    ).first()

    if not has_role:
        _assign_default_role(db, user)
    if not has_sub:
        _assign_free_plan(db, user)
    if not has_role or not has_sub:
        db.commit()


def _assign_default_role(db: Session, user: User) -> None:
    role = db.query(Role).filter(
        Role.is_default == True,  # noqa: E712
        Role.is_deleted == False,  # noqa: E712
    ).first()

    if not role:
        logger.warning("No default role found, skipping role assignment for user %s", user.id)
        return

    user_role = UserRole(
        id=str(uuid.uuid4()),
        user_id=user.id,
        role_id=role.id,
        created_by="SYSTEM",
    )
    db.add(user_role)
    logger.info("Assigned role '%s' to user %s", role.name, user.email)


def _assign_free_plan(db: Session, user: User) -> None:
    plan = db.query(Plan).filter(
        Plan.name == "free",
        Plan.is_active == True,  # noqa: E712
        Plan.is_deleted == False,  # noqa: E712
    ).first()

    if not plan:
        logger.warning("No free plan found, skipping subscription for user %s", user.id)
        return

    subscription = UserSubscription(
        id=str(uuid.uuid4()),
        user_id=user.id,
        plan_id=plan.id,
        status="active",
        started_at=datetime.now(timezone.utc),
        created_by="SYSTEM",
    )
    db.add(subscription)
    logger.info("Assigned free plan to user %s", user.email)
