import logging
from datetime import datetime, timezone

from src.domains.notifications.models import NotificationLog
from src.domains.nutrition.models import SupplyItem
from src.domains.cats.models import Cat
from src.utils.db import SessionLocal

logger = logging.getLogger(__name__)


def check_low_stock() -> None:
    db = SessionLocal()
    try:
        low_stock_items = (
            db.query(SupplyItem)
            .filter(
                SupplyItem.is_deleted == False,  # noqa: E712
                SupplyItem.current_quantity <= SupplyItem.low_stock_threshold,
            )
            .all()
        )

        for item in low_stock_items:
            cat = db.query(Cat).filter(Cat.id == item.cat_id).first()
            if not cat:
                continue

            notification = NotificationLog(
                user_id=cat.owner_id,
                notification_type="low_stock",
                message=f"Low stock alert: {item.name} ({item.current_quantity} {item.unit} remaining)",
                sent_at=datetime.now(timezone.utc),
                cat_id=cat.id,
            )
            db.add(notification)
            logger.info("low stock alert created", extra={"item": item.name, "cat_id": cat.id})

        db.commit()
    except Exception:
        logger.exception("error during low stock check")
        db.rollback()
    finally:
        db.close()
