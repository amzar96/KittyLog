from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class CatWeight(CoreModel, Base):
    __tablename__ = "catweight"
    __table_args__ = {"schema": "kittylog"}

    weight = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = Column(String, nullable=True)
    cat_id = Column(String, ForeignKey("kittylog.cat.id"), nullable=False)

    cat = relationship("Cat", back_populates="weights")


class CatVaccine(CoreModel, Base):
    __tablename__ = "catvaccine"
    __table_args__ = {"schema": "kittylog"}

    vaccine_name = Column(String, nullable=False)
    administered_at = Column(DateTime, nullable=False)
    next_due_at = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    cat_id = Column(String, ForeignKey("kittylog.cat.id"), nullable=False)

    cat = relationship("Cat", back_populates="vaccines")


class VetVisit(CoreModel, Base):
    __tablename__ = "vetvisit"
    __table_args__ = {"schema": "kittylog"}

    visit_date = Column(DateTime, nullable=False)
    clinic_name = Column(String, nullable=True)
    vet_name = Column(String, nullable=True)
    reason = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    cat_id = Column(String, ForeignKey("kittylog.cat.id"), nullable=False)

    cat = relationship("Cat")


class DailyHealth(CoreModel, Base):
    __tablename__ = "dailyhealth"
    __table_args__ = {"schema": "kittylog"}

    log_date = Column(DateTime, nullable=False)
    ate = Column(Boolean, default=False)
    ate_at = Column(DateTime, nullable=True)
    used_litter = Column(Boolean, default=False)
    used_litter_at = Column(DateTime, nullable=True)
    took_medicine = Column(Boolean, default=False)
    took_medicine_at = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    cat_id = Column(String, ForeignKey("kittylog.cat.id"), nullable=False)

    cat = relationship("Cat")
