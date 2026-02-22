from sqlalchemy import Boolean, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class Permission(CoreModel, Base):
    __tablename__ = "permission"
    __table_args__ = (
        UniqueConstraint("action", "resource", name="uq_permission_action_resource"),
    )

    action = Column(String, nullable=False, index=True)
    resource = Column(String, nullable=False, index=True)


class Role(CoreModel, Base):
    __tablename__ = "role"

    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)

    permissions = relationship("RolePermission", back_populates="role", lazy="joined")


class RolePermission(CoreModel, Base):
    __tablename__ = "role_permission"
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )

    role_id = Column(String, ForeignKey("role.id"), nullable=False)
    permission_id = Column(String, ForeignKey("permission.id"), nullable=False)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission")


class UserRole(CoreModel, Base):
    __tablename__ = "user_role"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role_id = Column(String, ForeignKey("role.id"), nullable=False)

    role = relationship("Role")
