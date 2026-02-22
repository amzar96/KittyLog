import logging
from datetime import datetime, timedelta, timezone

from src.domains.monitoring.models import ActivityLog
from src.utils.db import SessionLocal

logger = logging.getLogger(__name__)

ANOMALY_THRESHOLDS = {
    "meal": timedelta(hours=12),
    "litter": timedelta(hours=24),
    "medicine": timedelta(hours=24),
}


def check_anomalies() -> None:
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        for activity_type, threshold in ANOMALY_THRESHOLDS.items():
            cutoff = now - threshold

            recent = (
                db.query(ActivityLog)
                .filter(
                    ActivityLog.activity_type == activity_type,
                    ActivityLog.logged_at >= cutoff,
                    ActivityLog.is_deleted == False,  # noqa: E712
                )
                .all()
            )

            cat_ids_with_activity = {a.cat_id for a in recent}

            all_cats_with_type = (
                db.query(ActivityLog.cat_id)
                .filter(
                    ActivityLog.activity_type == activity_type,
                    ActivityLog.is_deleted == False,  # noqa: E712
                )
                .distinct()
                .all()
            )

            for (cat_id,) in all_cats_with_type:
                if cat_id not in cat_ids_with_activity:
                    anomaly = ActivityLog(
                        activity_type=activity_type,
                        logged_at=now,
                        is_anomaly=True,
                        anomaly_reason=f"No {activity_type} logged in the last {threshold}",
                        cat_id=cat_id,
                    )
                    db.add(anomaly)
                    logger.warning(
                        "anomaly detected",
                        extra={"cat_id": cat_id, "type": activity_type, "threshold": str(threshold)},
                    )

            db.commit()
    except Exception:
        logger.exception("error during anomaly detection")
        db.rollback()
    finally:
        db.close()
