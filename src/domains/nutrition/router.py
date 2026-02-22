import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.domains.nutrition.schemas import (
    StockLogCreate,
    StockLogResponse,
    SupplyItemCreate,
    SupplyItemResponse,
    SupplyItemUpdate,
)
from src.domains.nutrition.service import NutritionService
from src.shared.models.user import User
from src.shared.schemas.response import PaginatedResponse, ResponseModel
from src.utils.db import get_db

router = APIRouter(prefix="/cats/{cat_id}/supplies", tags=["nutrition"])
logger = logging.getLogger(__name__)


def get_nutrition_service(db: Session = Depends(get_db)) -> NutritionService:
    return NutritionService(db)


@router.get("", response_model=PaginatedResponse[SupplyItemResponse])
def list_supplies(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: NutritionService = Depends(get_nutrition_service),
):
    supplies = service.list_supplies(cat_id, user)
    return PaginatedResponse(data=supplies, total=len(supplies), page=1, page_size=len(supplies))


@router.post("", response_model=ResponseModel[SupplyItemResponse], status_code=status.HTTP_201_CREATED)
def create_supply(
    cat_id: str,
    payload: SupplyItemCreate,
    user: User = Depends(get_current_user),
    service: NutritionService = Depends(get_nutrition_service),
):
    item = service.create_supply(cat_id, payload, user)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=item, message="Supply item created successfully")


@router.put("/{supply_id}", response_model=ResponseModel[SupplyItemResponse])
def update_supply(
    cat_id: str,
    supply_id: str,
    payload: SupplyItemUpdate,
    user: User = Depends(get_current_user),
    service: NutritionService = Depends(get_nutrition_service),
):
    item = service.update_supply(cat_id, supply_id, payload, user)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply item not found")
    return ResponseModel(data=item, message="Supply item updated successfully")


@router.post("/{supply_id}/stock", response_model=ResponseModel[StockLogResponse], status_code=status.HTTP_201_CREATED)
def add_stock(
    cat_id: str,
    supply_id: str,
    payload: StockLogCreate,
    user: User = Depends(get_current_user),
    service: NutritionService = Depends(get_nutrition_service),
):
    log = service.add_stock(cat_id, supply_id, payload, user)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply item not found")
    return ResponseModel(data=log, message="Stock added successfully")


@router.get("/alerts", response_model=PaginatedResponse[SupplyItemResponse])
def get_low_stock_alerts(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: NutritionService = Depends(get_nutrition_service),
):
    items = service.get_low_stock_alerts(cat_id, user)
    return PaginatedResponse(data=items, total=len(items), page=1, page_size=len(items))
