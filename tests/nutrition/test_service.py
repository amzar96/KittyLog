from datetime import datetime, timezone

from src.domains.cats.schemas import CatCreate
from src.domains.cats.service import CatService
from src.domains.nutrition.schemas import StockLogCreate, SupplyItemCreate, SupplyItemUpdate
from src.domains.nutrition.service import NutritionService


class TestNutritionService:
    def _create_cat(self, db, user):
        service = CatService(db)
        return service.create_cat(CatCreate(name="NutriCat", nickname="nc"), user)

    def test_create_and_list_supplies(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = NutritionService(db)

        item = service.create_supply(
            cat.id,
            SupplyItemCreate(name="Royal Canin", category="kibble", unit="grams", current_quantity=500, low_stock_threshold=100),
            test_user,
        )
        assert item is not None
        assert item.name == "Royal Canin"

        supplies = service.list_supplies(cat.id, test_user)
        assert len(supplies) >= 1

        CatService(db).delete_cat(cat.id, test_user)

    def test_update_supply(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = NutritionService(db)

        item = service.create_supply(
            cat.id,
            SupplyItemCreate(name="Whiskas", category="wet_food", unit="cans", current_quantity=10),
            test_user,
        )

        updated = service.update_supply(cat.id, item.id, SupplyItemUpdate(low_stock_threshold=5), test_user)
        assert updated.low_stock_threshold == 5

        CatService(db).delete_cat(cat.id, test_user)

    def test_add_stock_updates_quantity(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = NutritionService(db)

        item = service.create_supply(
            cat.id,
            SupplyItemCreate(name="Medicine", category="medicine", unit="tablets", current_quantity=5),
            test_user,
        )

        log = service.add_stock(
            cat.id,
            item.id,
            StockLogCreate(quantity_added=10, purchased_at=datetime.now(timezone.utc)),
            test_user,
        )
        assert log is not None

        supplies = service.list_supplies(cat.id, test_user)
        updated_item = next(s for s in supplies if s.id == item.id)
        assert updated_item.current_quantity == 15

        CatService(db).delete_cat(cat.id, test_user)

    def test_low_stock_alerts(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = NutritionService(db)

        service.create_supply(
            cat.id,
            SupplyItemCreate(name="LowItem", category="kibble", unit="grams", current_quantity=5, low_stock_threshold=10),
            test_user,
        )

        alerts = service.get_low_stock_alerts(cat.id, test_user)
        assert len(alerts) >= 1

        CatService(db).delete_cat(cat.id, test_user)
