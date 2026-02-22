import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.domains.notifications.schemas import (
    NotificationLogResponse,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
)
from src.domains.notifications.service import NotificationService
from src.shared.models.user import User
from src.shared.rbac import require_permission
from src.shared.schemas.response import PaginatedResponse, ResponseModel
from src.utils.db import get_db

router = APIRouter(prefix="/notifications", tags=["notifications"])
logger = logging.getLogger(__name__)


def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(db)


@router.get("", response_model=PaginatedResponse[NotificationLogResponse])
def list_notifications(
    user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
    _: None = Depends(require_permission("can_read", "notification")),
):
    notifications = service.list_notifications(user)
    return PaginatedResponse(data=notifications, total=len(notifications), page=1, page_size=len(notifications))


@router.put("/{notification_id}/read", response_model=ResponseModel[NotificationLogResponse])
def mark_as_read(
    notification_id: str,
    user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
    _: None = Depends(require_permission("can_edit", "notification")),
):
    notification = service.mark_as_read(notification_id, user)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return ResponseModel(data=notification, message="Notification marked as read")


@router.get("/preferences", response_model=ResponseModel[NotificationPreferenceResponse])
def get_preferences(
    user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
    _: None = Depends(require_permission("can_read", "notification")),
):
    pref = service.get_preferences(user)
    return ResponseModel(data=pref, message="success")


@router.put("/preferences", response_model=ResponseModel[NotificationPreferenceResponse])
def update_preferences(
    payload: NotificationPreferenceUpdate,
    user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
    _: None = Depends(require_permission("can_edit", "notification")),
):
    pref = service.update_preferences(user, payload)
    return ResponseModel(data=pref, message="Preferences updated successfully")
