from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class Plan(CoreModel, Base):
    __tablename__ = "plan"

    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, default=0.0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    permissions = relationship("PlanPermission", back_populates="plan", lazy="joined")


class PlanPermission(CoreModel, Base):
    __tablename__ = "plan_permission"
    __table_args__ = (
        UniqueConstraint("plan_id", "permission_id", name="uq_plan_permission"),
    )

    plan_id = Column(String, ForeignKey("plan.id"), nullable=False)
    permission_id = Column(String, ForeignKey("permission.id"), nullable=False)

    plan = relationship("Plan", back_populates="permissions")
    permission = relationship("Permission")


class UserSubscription(CoreModel, Base):
    __tablename__ = "user_subscription"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan_id = Column(String, ForeignKey("plan.id"), nullable=False)
    status = Column(String, default="active", nullable=False)
    started_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    plan = relationship("Plan")
