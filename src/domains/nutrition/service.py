import logging

from sqlalchemy.orm import Session

from src.domains.cats.models import Cat
from src.domains.nutrition.models import StockLog, SupplyItem
from src.domains.nutrition.schemas import StockLogCreate, SupplyItemCreate, SupplyItemUpdate
from src.shared.models.user import User

logger = logging.getLogger(__name__)


class NutritionService:
    def __init__(self, db: Session):
        self.db = db

    def _get_cat(self, cat_id: str, user: User) -> Cat | None:
        return (
            self.db.query(Cat)
            .filter(Cat.id == cat_id, Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .first()
        )

    def list_supplies(self, cat_id: str, user: User) -> list[SupplyItem]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []
        return (
            self.db.query(SupplyItem)
            .filter(SupplyItem.cat_id == cat_id, SupplyItem.is_deleted == False)  # noqa: E712
            .order_by(SupplyItem.name)
            .all()
        )

    def create_supply(self, cat_id: str, payload: SupplyItemCreate, user: User) -> SupplyItem | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        item = SupplyItem(**payload.model_dump(), cat_id=cat_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        logger.info("supply item created", extra={"cat_id": cat_id, "item": payload.name})
        return item

    def update_supply(self, cat_id: str, supply_id: str, payload: SupplyItemUpdate, user: User) -> SupplyItem | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        item = (
            self.db.query(SupplyItem)
            .filter(SupplyItem.id == supply_id, SupplyItem.cat_id == cat_id, SupplyItem.is_deleted == False)  # noqa: E712
            .first()
        )
        if not item:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, field, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def add_stock(self, cat_id: str, supply_id: str, payload: StockLogCreate, user: User) -> StockLog | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        item = (
            self.db.query(SupplyItem)
            .filter(SupplyItem.id == supply_id, SupplyItem.cat_id == cat_id, SupplyItem.is_deleted == False)  # noqa: E712
            .first()
        )
        if not item:
            return None

        log = StockLog(**payload.model_dump(), supply_item_id=supply_id)
        self.db.add(log)

        item.current_quantity += payload.quantity_added
        self.db.commit()
        self.db.refresh(log)
        logger.info("stock added", extra={"supply_id": supply_id, "quantity": payload.quantity_added})
        return log

    def get_low_stock_alerts(self, cat_id: str, user: User) -> list[SupplyItem]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []
        return (
            self.db.query(SupplyItem)
            .filter(
                SupplyItem.cat_id == cat_id,
                SupplyItem.is_deleted == False,  # noqa: E712
                SupplyItem.current_quantity <= SupplyItem.low_stock_threshold,
            )
            .all()
        )
