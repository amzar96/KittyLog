import logging

from sqlalchemy.orm import Session

from src.domains.cats.models import Cat
from src.domains.monitoring.models import ActivityLog
from src.domains.monitoring.schemas import ActivityLogCreate, CatStatusResponse
from src.shared.models.user import User

logger = logging.getLogger(__name__)


class MonitoringService:
    def __init__(self, db: Session):
        self.db = db

    def _get_cat(self, cat_id: str, user: User) -> Cat | None:
        return (
            self.db.query(Cat)
            .filter(Cat.id == cat_id, Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .first()
        )

    def list_activities(self, cat_id: str, user: User, activity_type: str | None = None) -> list[ActivityLog]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []

        query = self.db.query(ActivityLog).filter(
            ActivityLog.cat_id == cat_id,
            ActivityLog.is_deleted == False,  # noqa: E712
        )
        if activity_type:
            query = query.filter(ActivityLog.activity_type == activity_type)

        return query.order_by(ActivityLog.logged_at.desc()).all()

    def create_activity(self, cat_id: str, payload: ActivityLogCreate, user: User) -> ActivityLog | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        activity = ActivityLog(**payload.model_dump(), cat_id=cat_id)
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        logger.info("activity logged", extra={"cat_id": cat_id, "type": payload.activity_type})
        return activity

    def get_cat_status(self, cat_id: str, user: User) -> CatStatusResponse | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        def _last_activity(activity_type: str):
            result = (
                self.db.query(ActivityLog)
                .filter(
                    ActivityLog.cat_id == cat_id,
                    ActivityLog.activity_type == activity_type,
                    ActivityLog.is_deleted == False,  # noqa: E712
                )
                .order_by(ActivityLog.logged_at.desc())
                .first()
            )
            return result.logged_at if result else None

        return CatStatusResponse(
            cat_id=cat_id,
            last_meal_at=_last_activity("meal"),
            last_litter_at=_last_activity("litter"),
            last_medicine_at=_last_activity("medicine"),
            last_play_at=_last_activity("play"),
        )

    def list_anomalies(self, cat_id: str, user: User) -> list[ActivityLog]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []
        return (
            self.db.query(ActivityLog)
            .filter(
                ActivityLog.cat_id == cat_id,
                ActivityLog.is_anomaly == True,  # noqa: E712
                ActivityLog.is_deleted == False,  # noqa: E712
            )
            .order_by(ActivityLog.logged_at.desc())
            .all()
        )
