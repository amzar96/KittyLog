import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_current_user
from src.domains.appointments.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
    ReminderCreate,
    ReminderResponse,
)
from src.domains.appointments.service import AppointmentService
from src.shared.models.user import User
from src.shared.schemas.response import PaginatedResponse, ResponseModel
from src.utils.db import get_db

router = APIRouter(prefix="/cats/{cat_id}/appointments", tags=["appointments"])
logger = logging.getLogger(__name__)


def get_appointment_service(db: Session = Depends(get_db)) -> AppointmentService:
    return AppointmentService(db)


@router.get("", response_model=PaginatedResponse[AppointmentResponse])
def list_appointments(
    cat_id: str,
    user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    appointments = service.list_appointments(cat_id, user)
    return PaginatedResponse(data=appointments, total=len(appointments), page=1, page_size=len(appointments))


@router.get("/{appointment_id}", response_model=ResponseModel[AppointmentResponse])
def get_appointment(
    cat_id: str,
    appointment_id: str,
    user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    appointment = service.get_appointment(cat_id, appointment_id, user)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return ResponseModel(data=appointment, message="success")


@router.post("", response_model=ResponseModel[AppointmentResponse], status_code=status.HTTP_201_CREATED)
def create_appointment(
    cat_id: str,
    payload: AppointmentCreate,
    user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    appointment = service.create_appointment(cat_id, payload, user)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return ResponseModel(data=appointment, message="Appointment created successfully")


@router.put("/{appointment_id}", response_model=ResponseModel[AppointmentResponse])
def update_appointment(
    cat_id: str,
    appointment_id: str,
    payload: AppointmentUpdate,
    user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    appointment = service.update_appointment(cat_id, appointment_id, payload, user)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return ResponseModel(data=appointment, message="Appointment updated successfully")


@router.delete("/{appointment_id}", response_model=ResponseModel)
def delete_appointment(
    cat_id: str,
    appointment_id: str,
    user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    deleted = service.delete_appointment(cat_id, appointment_id, user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return ResponseModel(data=None, message="Appointment deleted successfully")


@router.post("/{appointment_id}/reminders", response_model=ResponseModel[ReminderResponse], status_code=status.HTTP_201_CREATED)
def add_reminder(
    cat_id: str,
    appointment_id: str,
    payload: ReminderCreate,
    user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    reminder = service.add_reminder(cat_id, appointment_id, payload, user)
    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return ResponseModel(data=reminder, message="Reminder added successfully")
