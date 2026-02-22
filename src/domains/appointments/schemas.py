from datetime import datetime

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    appointment_type: str
    scheduled_at: datetime
    location: str | None = None
    notes: str | None = None


class AppointmentUpdate(BaseModel):
    scheduled_at: datetime | None = None
    location: str | None = None
    notes: str | None = None
    is_completed: bool | None = None


class AppointmentResponse(BaseModel):
    id: str
    appointment_type: str
    scheduled_at: datetime
    location: str | None
    notes: str | None
    is_completed: bool
    google_calendar_event_id: str | None
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReminderCreate(BaseModel):
    remind_at: datetime
    message: str


class ReminderResponse(BaseModel):
    id: str
    remind_at: datetime
    message: str
    is_sent: bool
    appointment_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
