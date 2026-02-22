from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class ActivityLog(CoreModel, Base):
    __tablename__ = "activitylog"

    activity_type = Column(String, nullable=False)  # meal, litter, medicine, play
    logged_at = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    anomaly_reason = Column(String, nullable=True)
    cat_id = Column(String, ForeignKey("cat.id"), nullable=False)

    cat = relationship("Cat")
