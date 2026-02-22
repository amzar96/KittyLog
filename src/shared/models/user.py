from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class User(CoreModel, Base):
    __tablename__ = "users"

    full_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    picture_url = Column(String, nullable=True)

    cats = relationship("Cat", back_populates="owner")
