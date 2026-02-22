import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, MetaData, String
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(schema=settings.DB_SCHEMA)


class CoreModel:
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_by = Column(String, default="SYSTEM", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_by = Column(String, nullable=True)
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
