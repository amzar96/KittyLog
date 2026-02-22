from datetime import datetime, timezone

from src.domains.cats.schemas import CatCreate
from src.domains.cats.service import CatService
from src.domains.monitoring.schemas import ActivityLogCreate
from src.domains.monitoring.service import MonitoringService


class TestMonitoringService:
    def _create_cat(self, db, user):
        service = CatService(db)
        return service.create_cat(CatCreate(name="MonitorCat", nickname="mc"), user)

    def test_create_and_list_activities(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = MonitoringService(db)

        activity = service.create_activity(
            cat.id,
            ActivityLogCreate(activity_type="meal", logged_at=datetime.now(timezone.utc)),
            test_user,
        )
        assert activity is not None
        assert activity.activity_type == "meal"

        activities = service.list_activities(cat.id, test_user)
        assert len(activities) >= 1

        CatService(db).delete_cat(cat.id, test_user)

    def test_filter_activities_by_type(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = MonitoringService(db)

        now = datetime.now(timezone.utc)
        service.create_activity(cat.id, ActivityLogCreate(activity_type="meal", logged_at=now), test_user)
        service.create_activity(cat.id, ActivityLogCreate(activity_type="play", logged_at=now), test_user)

        meals = service.list_activities(cat.id, test_user, activity_type="meal")
        assert all(a.activity_type == "meal" for a in meals)

        CatService(db).delete_cat(cat.id, test_user)

    def test_get_cat_status(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = MonitoringService(db)

        now = datetime.now(timezone.utc)
        service.create_activity(cat.id, ActivityLogCreate(activity_type="meal", logged_at=now), test_user)

        status = service.get_cat_status(cat.id, test_user)
        assert status is not None
        assert status.last_meal_at is not None

        CatService(db).delete_cat(cat.id, test_user)

    def test_get_status_for_nonexistent_cat(self, db, test_user):
        service = MonitoringService(db)
        status = service.get_cat_status("fake-id", test_user)
        assert status is None
