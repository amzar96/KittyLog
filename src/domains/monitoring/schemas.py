from datetime import datetime

from pydantic import BaseModel


class ActivityLogCreate(BaseModel):
    activity_type: str
    logged_at: datetime
    quantity: float | None = None
    notes: str | None = None


class ActivityLogResponse(BaseModel):
    id: str
    activity_type: str
    logged_at: datetime
    quantity: float | None
    notes: str | None
    is_anomaly: bool
    anomaly_reason: str | None
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CatStatusResponse(BaseModel):
    cat_id: str
    last_meal_at: datetime | None
    last_litter_at: datetime | None
    last_medicine_at: datetime | None
    last_play_at: datetime | None
