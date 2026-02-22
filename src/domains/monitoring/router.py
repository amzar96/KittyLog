import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.domains.monitoring.schemas import ActivityLogCreate, ActivityLogResponse, CatStatusResponse
from src.domains.monitoring.service import MonitoringService
from src.shared.models.user import User
from src.shared.schemas.response import PaginatedResponse, ResponseModel
from src.utils.db import get_db

router = APIRouter(prefix="/cats/{cat_id}", tags=["monitoring"])
logger = logging.getLogger(__name__)


def get_monitoring_service(db: Session = Depends(get_db)) -> MonitoringService:
    return MonitoringService(db)


@router.get("/activities", response_model=PaginatedResponse[ActivityLogResponse])
def list_activities(
    cat_id: str,
    activity_type: str | None = Query(default=None),
    user: User = Depends(get_current_user),
    service: MonitoringService = Depends(get_monitoring_service),
):
    activities = service.list_activities(cat_id, user, activity_type)
    return PaginatedResponse(data=activities, total=len(activities), page=1, page_size=len(activities))


@router.post("/activities", response_model=ResponseModel[ActivityLogResponse], status_code=status.HTTP_201_CREATED)
def create_activity(
    cat_id: str,
    payload: ActivityLogCreate,
    user: User = Depends(get_current_user),
    service: MonitoringService = Depends(get_monitoring_service),
):
    activity = service.create_activity(cat_id, payload, user)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=activity, message="Activity logged successfully")


@router.get("/status", response_model=ResponseModel[CatStatusResponse])
def get_cat_status(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: MonitoringService = Depends(get_monitoring_service),
):
    cat_status = service.get_cat_status(cat_id, user)
    if not cat_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=cat_status, message="success")


@router.get("/anomalies", response_model=PaginatedResponse[ActivityLogResponse])
def list_anomalies(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: MonitoringService = Depends(get_monitoring_service),
):
    anomalies = service.list_anomalies(cat_id, user)
    return PaginatedResponse(data=anomalies, total=len(anomalies), page=1, page_size=len(anomalies))
