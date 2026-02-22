from datetime import datetime, timezone

from src.domains.appointments.schemas import AppointmentCreate, AppointmentUpdate, ReminderCreate
from src.domains.appointments.service import AppointmentService
from src.domains.cats.schemas import CatCreate
from src.domains.cats.service import CatService


class TestAppointmentService:
    def _create_cat(self, db, user):
        service = CatService(db)
        return service.create_cat(CatCreate(name="ApptCat", nickname="ac"), user)

    def test_create_and_list_appointments(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = AppointmentService(db)

        appt = service.create_appointment(
            cat.id,
            AppointmentCreate(appointment_type="vet", scheduled_at=datetime.now(timezone.utc)),
            test_user,
        )
        assert appt is not None
        assert appt.appointment_type == "vet"

        appointments = service.list_appointments(cat.id, test_user)
        assert len(appointments) >= 1

        CatService(db).delete_cat(cat.id, test_user)

    def test_update_appointment(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = AppointmentService(db)

        appt = service.create_appointment(
            cat.id,
            AppointmentCreate(appointment_type="grooming", scheduled_at=datetime.now(timezone.utc)),
            test_user,
        )

        updated = service.update_appointment(cat.id, appt.id, AppointmentUpdate(is_completed=True), test_user)
        assert updated.is_completed is True

        CatService(db).delete_cat(cat.id, test_user)

    def test_delete_appointment(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = AppointmentService(db)

        appt = service.create_appointment(
            cat.id,
            AppointmentCreate(appointment_type="vet", scheduled_at=datetime.now(timezone.utc)),
            test_user,
        )

        result = service.delete_appointment(cat.id, appt.id, test_user)
        assert result is True

        found = service.get_appointment(cat.id, appt.id, test_user)
        assert found is None

        CatService(db).delete_cat(cat.id, test_user)

    def test_add_reminder(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = AppointmentService(db)

        appt = service.create_appointment(
            cat.id,
            AppointmentCreate(appointment_type="vet", scheduled_at=datetime.now(timezone.utc)),
            test_user,
        )

        reminder = service.add_reminder(
            cat.id,
            appt.id,
            ReminderCreate(remind_at=datetime.now(timezone.utc), message="Don't forget!"),
            test_user,
        )
        assert reminder is not None
        assert reminder.message == "Don't forget!"

        CatService(db).delete_cat(cat.id, test_user)
