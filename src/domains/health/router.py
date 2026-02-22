import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.domains.health.schemas import (
    DailyHealthCreate,
    DailyHealthResponse,
    DailyHealthUpdate,
    VaccineCreate,
    VaccineResponse,
    VetVisitCreate,
    VetVisitResponse,
    WeightCreate,
    WeightResponse,
)
from src.domains.health.service import HealthService
from src.shared.models.user import User
from src.shared.schemas.response import PaginatedResponse, ResponseModel
from src.utils.db import get_db

router = APIRouter(prefix="/cats/{cat_id}", tags=["health"])
logger = logging.getLogger(__name__)


def get_health_service(db: Session = Depends(get_db)) -> HealthService:
    return HealthService(db)


# Weight endpoints
@router.get("/weights", response_model=PaginatedResponse[WeightResponse])
def list_weights(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    weights = service.list_weights(cat_id, user)
    return PaginatedResponse(data=weights, total=len(weights), page=1, page_size=len(weights))


@router.post("/weights", response_model=ResponseModel[WeightResponse], status_code=status.HTTP_201_CREATED)
def create_weight(
    cat_id: str,
    payload: WeightCreate,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    weight = service.create_weight(cat_id, payload, user)
    if not weight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=weight, message="Weight recorded successfully")


# Vaccine endpoints
@router.get("/vaccines", response_model=PaginatedResponse[VaccineResponse])
def list_vaccines(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    vaccines = service.list_vaccines(cat_id, user)
    return PaginatedResponse(data=vaccines, total=len(vaccines), page=1, page_size=len(vaccines))


@router.post("/vaccines", response_model=ResponseModel[VaccineResponse], status_code=status.HTTP_201_CREATED)
def create_vaccine(
    cat_id: str,
    payload: VaccineCreate,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    vaccine = service.create_vaccine(cat_id, payload, user)
    if not vaccine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=vaccine, message="Vaccine recorded successfully")


# Vet visit endpoints
@router.get("/vet-visits", response_model=PaginatedResponse[VetVisitResponse])
def list_vet_visits(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    visits = service.list_vet_visits(cat_id, user)
    return PaginatedResponse(data=visits, total=len(visits), page=1, page_size=len(visits))


@router.post("/vet-visits", response_model=ResponseModel[VetVisitResponse], status_code=status.HTTP_201_CREATED)
def create_vet_visit(
    cat_id: str,
    payload: VetVisitCreate,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    visit = service.create_vet_visit(cat_id, payload, user)
    if not visit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=visit, message="Vet visit recorded successfully")


# Daily health endpoints
@router.get("/daily-health", response_model=ResponseModel[DailyHealthResponse])
def get_daily_health(
    cat_id: str,
    log_date: datetime = Query(...),
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    health = service.get_daily_health(cat_id, log_date, user)
    if not health:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily health log not found")
    return ResponseModel(data=health, message="success")


@router.post("/daily-health", response_model=ResponseModel[DailyHealthResponse], status_code=status.HTTP_201_CREATED)
def create_daily_health(
    cat_id: str,
    payload: DailyHealthCreate,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    health = service.create_daily_health(cat_id, payload, user)
    if not health:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=health, message="Daily health logged successfully")


@router.put("/daily-health/{health_id}", response_model=ResponseModel[DailyHealthResponse])
def update_daily_health(
    cat_id: str,
    health_id: str,
    payload: DailyHealthUpdate,
    user: User = Depends(get_current_user),
    service: HealthService = Depends(get_health_service),
):
    health = service.update_daily_health(cat_id, health_id, payload, user)
    if not health:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily health log not found")
    return ResponseModel(data=health, message="Daily health updated successfully")
