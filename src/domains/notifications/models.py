from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class NotificationPreference(CoreModel, Base):
    __tablename__ = "notificationpreference"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    low_stock_alerts = Column(Boolean, default=True)
    vaccination_reminders = Column(Boolean, default=True)
    appointment_reminders = Column(Boolean, default=True)
    missed_activity_alerts = Column(Boolean, default=True)
    reminder_advance_hours = Column(Integer, default=24)

    user = relationship("User")


class NotificationLog(CoreModel, Base):
    __tablename__ = "notificationlog"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    notification_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime, nullable=False)
    is_read = Column(Boolean, default=False)
    cat_id = Column(String, ForeignKey("cat.id"), nullable=True)

    user = relationship("User")
    cat = relationship("Cat")
