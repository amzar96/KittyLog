from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared.models.base import Base, CoreModel


class SupplyItem(CoreModel, Base):
    __tablename__ = "supplyitem"
    __table_args__ = {"schema": "kittylog"}

    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # kibble, wet_food, medicine
    unit = Column(String, nullable=False)  # grams, cans, tablets
    current_quantity = Column(Float, nullable=False, default=0)
    low_stock_threshold = Column(Float, nullable=False, default=0)
    cat_id = Column(String, ForeignKey("kittylog.cat.id"), nullable=False)

    cat = relationship("Cat")
    stock_logs = relationship("StockLog", back_populates="supply_item")


class StockLog(CoreModel, Base):
    __tablename__ = "stocklog"
    __table_args__ = {"schema": "kittylog"}

    quantity_added = Column(Float, nullable=False)
    purchased_at = Column(DateTime, nullable=False)
    price = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    supply_item_id = Column(String, ForeignKey("kittylog.supplyitem.id"), nullable=False)

    supply_item = relationship("SupplyItem", back_populates="stock_logs")
