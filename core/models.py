import uuid
import datetime
from database.db import Base
from sqlalchemy import Boolean, Column, String, DateTime


class CoreModel:
    id = Column(String, primary_key=True, default=uuid.uuid4, index=True)
    created_by = Column(String, default="SYSTEM", nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_by = Column(String, default=None, nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, nullable=False)
    is_deleted = Column(Boolean, default=False)


class User(Base, CoreModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)


class Cat(Base, CoreModel):
    __tablename__ = "cat"

    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
