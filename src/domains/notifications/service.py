import logging

from sqlalchemy.orm import Session

from src.domains.notifications.models import NotificationLog, NotificationPreference
from src.domains.notifications.schemas import NotificationPreferenceUpdate
from src.shared.models.user import User

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_preferences(self, user: User) -> NotificationPreference:
        pref = (
            self.db.query(NotificationPreference)
            .filter(NotificationPreference.user_id == user.id, NotificationPreference.is_deleted == False)  # noqa: E712
            .first()
        )
        if not pref:
            pref = NotificationPreference(user_id=user.id)
            self.db.add(pref)
            self.db.commit()
            self.db.refresh(pref)
        return pref

    def update_preferences(self, user: User, payload: NotificationPreferenceUpdate) -> NotificationPreference:
        pref = self.get_preferences(user)

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(pref, field, value)

        self.db.commit()
        self.db.refresh(pref)
        return pref

    def list_notifications(self, user: User) -> list[NotificationLog]:
        return (
            self.db.query(NotificationLog)
            .filter(NotificationLog.user_id == user.id, NotificationLog.is_deleted == False)  # noqa: E712
            .order_by(NotificationLog.sent_at.desc())
            .all()
        )

    def mark_as_read(self, notification_id: str, user: User) -> NotificationLog | None:
        notification = (
            self.db.query(NotificationLog)
            .filter(
                NotificationLog.id == notification_id,
                NotificationLog.user_id == user.id,
                NotificationLog.is_deleted == False,  # noqa: E712
            )
            .first()
        )
        if not notification:
            return None

        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return notification
