from datetime import datetime

from pydantic import BaseModel


class SupplyItemCreate(BaseModel):
    name: str
    category: str
    unit: str
    current_quantity: float = 0
    low_stock_threshold: float = 0


class SupplyItemUpdate(BaseModel):
    name: str | None = None
    current_quantity: float | None = None
    low_stock_threshold: float | None = None


class SupplyItemResponse(BaseModel):
    id: str
    name: str
    category: str
    unit: str
    current_quantity: float
    low_stock_threshold: float
    cat_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class StockLogCreate(BaseModel):
    quantity_added: float
    purchased_at: datetime
    price: float | None = None
    notes: str | None = None


class StockLogResponse(BaseModel):
    id: str
    quantity_added: float
    purchased_at: datetime
    price: float | None
    notes: str | None
    supply_item_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
