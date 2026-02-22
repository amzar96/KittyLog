import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.shared.models.rbac import Permission, Role, RolePermission, UserRole
from src.shared.models.subscription import PlanPermission, UserSubscription
from src.shared.models.user import User
from src.utils.db import get_db

logger = logging.getLogger(__name__)


def require_permission(action: str, resource: str):
    def permission_dependency(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> None:
        user_role = db.query(UserRole).filter(
            UserRole.user_id == user.id,
            UserRole.is_deleted == False,  # noqa: E712
        ).first()

        if not user_role:
            logger.warning("User %s has no role assigned", user.id)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned",
            )

        role = db.query(Role).filter(
            Role.id == user_role.role_id,
            Role.is_deleted == False,  # noqa: E712
        ).first()

        if role and role.name == "admin":
            return

        permission = db.query(Permission).filter(
            Permission.action == action,
            Permission.resource == resource,
            Permission.is_deleted == False,  # noqa: E712
        ).first()

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission {action} on {resource} does not exist",
            )

        role_has_permission = db.query(RolePermission).filter(
            RolePermission.role_id == user_role.role_id,
            RolePermission.permission_id == permission.id,
            RolePermission.is_deleted == False,  # noqa: E712
        ).first()

        if not role_has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == "active",
            UserSubscription.is_deleted == False,  # noqa: E712
        ).first()

        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No active subscription",
            )

        plan_has_permission = db.query(PlanPermission).filter(
            PlanPermission.plan_id == subscription.plan_id,
            PlanPermission.permission_id == permission.id,
            PlanPermission.is_deleted == False,  # noqa: E712
        ).first()

        if not plan_has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your plan does not include this feature",
            )

    return permission_dependency
