from datetime import datetime

from pydantic import BaseModel


class NotificationPreferenceUpdate(BaseModel):
    low_stock_alerts: bool | None = None
    vaccination_reminders: bool | None = None
    appointment_reminders: bool | None = None
    missed_activity_alerts: bool | None = None
    reminder_advance_hours: int | None = None


class NotificationPreferenceResponse(BaseModel):
    id: str
    user_id: str
    low_stock_alerts: bool
    vaccination_reminders: bool
    appointment_reminders: bool
    missed_activity_alerts: bool
    reminder_advance_hours: int
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationLogResponse(BaseModel):
    id: str
    user_id: str
    notification_type: str
    message: str
    sent_at: datetime
    is_read: bool
    cat_id: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
