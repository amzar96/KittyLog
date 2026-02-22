from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class Cat(CoreModel, Base):
    __tablename__ = "cat"

    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    dob = Column(DateTime, nullable=True)
    breed = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    color = Column(String, nullable=True)
    microchip_number = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="cats")
    weights = relationship("CatWeight", back_populates="cat")
    vaccines = relationship("CatVaccine", back_populates="cat")
