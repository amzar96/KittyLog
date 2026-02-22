from datetime import datetime

from pydantic import BaseModel


class CatCreate(BaseModel):
    name: str
    nickname: str
    dob: datetime | None = None
    breed: str | None = None
    gender: str | None = None
    color: str | None = None
    microchip_number: str | None = None


class CatUpdate(BaseModel):
    nickname: str | None = None
    dob: datetime | None = None
    breed: str | None = None
    gender: str | None = None
    color: str | None = None
    microchip_number: str | None = None


class CatResponse(BaseModel):
    id: str
    name: str
    nickname: str
    dob: datetime | None
    breed: str | None
    gender: str | None
    color: str | None
    microchip_number: str | None
    owner_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
