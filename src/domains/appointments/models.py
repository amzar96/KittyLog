from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class Appointment(CoreModel, Base):
    __tablename__ = "appointment"
    __table_args__ = {"schema": "kittylog"}

    appointment_type = Column(String, nullable=False)  # vet, grooming
    scheduled_at = Column(DateTime, nullable=False)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    google_calendar_event_id = Column(String, nullable=True)
    cat_id = Column(String, ForeignKey("kittylog.cat.id"), nullable=False)

    cat = relationship("Cat")
    reminders = relationship("Reminder", back_populates="appointment")


class Reminder(CoreModel, Base):
    __tablename__ = "reminder"
    __table_args__ = {"schema": "kittylog"}

    remind_at = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    is_sent = Column(Boolean, default=False)
    appointment_id = Column(String, ForeignKey("kittylog.appointment.id"), nullable=False)

    appointment = relationship("Appointment", back_populates="reminders")
