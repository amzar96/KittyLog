from datetime import datetime

from pydantic import BaseModel


class DiaryEntryCreate(BaseModel):
    entry_date: datetime
    title: str | None = None
    content: str
    mood: str | None = None
    photo_urls: str | None = None


class DiaryEntryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    mood: str | None = None
    photo_urls: str | None = None


class DiaryEntryResponse(BaseModel):
    id: str
    entry_date: datetime
    title: str | None
    content: str
    mood: str | None
    photo_urls: str | None
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
