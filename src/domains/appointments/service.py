import logging

from sqlalchemy.orm import Session

from src.domains.appointments.models import Appointment, Reminder
from src.domains.appointments.schemas import AppointmentCreate, AppointmentUpdate, ReminderCreate
from src.domains.cats.models import Cat
from src.shared.models.user import User

logger = logging.getLogger(__name__)


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def _get_cat(self, cat_id: str, user: User) -> Cat | None:
        return (
            self.db.query(Cat)
            .filter(Cat.id == cat_id, Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .first()
        )

    def list_appointments(self, cat_id: str, user: User) -> list[Appointment]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []
        return (
            self.db.query(Appointment)
            .filter(Appointment.cat_id == cat_id, Appointment.is_deleted == False)  # noqa: E712
            .order_by(Appointment.scheduled_at.desc())
            .all()
        )

    def get_appointment(self, cat_id: str, appointment_id: str, user: User) -> Appointment | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None
        return (
            self.db.query(Appointment)
            .filter(
                Appointment.id == appointment_id,
                Appointment.cat_id == cat_id,
                Appointment.is_deleted == False,  # noqa: E712
            )
            .first()
        )

    def create_appointment(self, cat_id: str, payload: AppointmentCreate, user: User) -> Appointment | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        appointment = Appointment(**payload.model_dump(), cat_id=cat_id)
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        logger.info("appointment created", extra={"cat_id": cat_id, "type": payload.appointment_type})
        return appointment

    def update_appointment(
        self, cat_id: str, appointment_id: str, payload: AppointmentUpdate, user: User
    ) -> Appointment | None:
        appointment = self.get_appointment(cat_id, appointment_id, user)
        if not appointment:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(appointment, field, value)

        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def delete_appointment(self, cat_id: str, appointment_id: str, user: User) -> bool:
        appointment = self.get_appointment(cat_id, appointment_id, user)
        if not appointment:
            return False

        appointment.is_deleted = True
        self.db.commit()
        return True

    def add_reminder(self, cat_id: str, appointment_id: str, payload: ReminderCreate, user: User) -> Reminder | None:
        appointment = self.get_appointment(cat_id, appointment_id, user)
        if not appointment:
            return None

        reminder = Reminder(**payload.model_dump(), appointment_id=appointment_id)
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        logger.info("reminder added", extra={"appointment_id": appointment_id})
        return reminder
