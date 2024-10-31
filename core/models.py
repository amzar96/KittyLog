import uuid
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, String, DateTime, Float, ForeignKey

Base = declarative_base()


class CoreModel:
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_by = Column(String, default="SYSTEM", nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_by = Column(String, default=None, nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, nullable=True)
    is_deleted = Column(Boolean, default=False)


class User(CoreModel, Base):
    __tablename__ = "users"

    full_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    cat = relationship("Cat", back_populates="owner")


class Cat(CoreModel, Base):
    __tablename__ = "cat"

    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    dob = Column(DateTime, nullable=True)
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="cat")
    weights = relationship("CatWeight", back_populates="cat")
    vaccines = relationship("CatVaccine", back_populates="cat")


class CatWeight(CoreModel, Base):
    __tablename__ = "catweight"

    weight = Column(Float, nullable=False)
    cat_id = Column(String, ForeignKey("cat.id"))
    cat = relationship("Cat", back_populates="weights")


class CatVaccine(CoreModel, Base):
    __tablename__ = "catvaccine"

    vaccine_name = Column(String, nullable=False)
    cat_id = Column(String, ForeignKey("cat.id"))
    cat = relationship("Cat", back_populates="vaccines")
