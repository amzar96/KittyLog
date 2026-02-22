from datetime import datetime

from pydantic import BaseModel


class WeightCreate(BaseModel):
    weight: float
    recorded_at: datetime | None = None
    notes: str | None = None


class WeightResponse(BaseModel):
    id: str
    weight: float
    recorded_at: datetime
    notes: str | None
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VaccineCreate(BaseModel):
    vaccine_name: str
    administered_at: datetime
    next_due_at: datetime | None = None
    notes: str | None = None


class VaccineResponse(BaseModel):
    id: str
    vaccine_name: str
    administered_at: datetime
    next_due_at: datetime | None
    notes: str | None
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VetVisitCreate(BaseModel):
    visit_date: datetime
    clinic_name: str | None = None
    vet_name: str | None = None
    reason: str
    notes: str | None = None


class VetVisitResponse(BaseModel):
    id: str
    visit_date: datetime
    clinic_name: str | None
    vet_name: str | None
    reason: str
    notes: str | None
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DailyHealthCreate(BaseModel):
    log_date: datetime
    ate: bool = False
    ate_at: datetime | None = None
    used_litter: bool = False
    used_litter_at: datetime | None = None
    took_medicine: bool = False
    took_medicine_at: datetime | None = None
    notes: str | None = None


class DailyHealthUpdate(BaseModel):
    ate: bool | None = None
    ate_at: datetime | None = None
    used_litter: bool | None = None
    used_litter_at: datetime | None = None
    took_medicine: bool | None = None
    took_medicine_at: datetime | None = None
    notes: str | None = None


class DailyHealthResponse(BaseModel):
    id: str
    log_date: datetime
    ate: bool
    ate_at: datetime | None
    used_litter: bool
    used_litter_at: datetime | None
    took_medicine: bool
    took_medicine_at: datetime | None
    notes: str | None
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
