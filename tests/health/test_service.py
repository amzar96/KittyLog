from datetime import datetime, timezone

from src.domains.cats.schemas import CatCreate
from src.domains.cats.service import CatService
from src.domains.health.schemas import VaccineCreate, VetVisitCreate, WeightCreate
from src.domains.health.service import HealthService


class TestHealthService:
    def _create_cat(self, db, user):
        service = CatService(db)
        return service.create_cat(CatCreate(name="HealthCat", nickname="hc"), user)

    def test_create_and_list_weights(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = HealthService(db)

        weight = service.create_weight(cat.id, WeightCreate(weight=4.5), test_user)
        assert weight is not None
        assert weight.weight == 4.5

        weights = service.list_weights(cat.id, test_user)
        assert len(weights) >= 1

        CatService(db).delete_cat(cat.id, test_user)

    def test_create_weight_for_nonexistent_cat(self, db, test_user):
        service = HealthService(db)
        result = service.create_weight("fake-id", WeightCreate(weight=3.0), test_user)
        assert result is None

    def test_create_and_list_vaccines(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = HealthService(db)

        now = datetime.now(timezone.utc)
        vaccine = service.create_vaccine(
            cat.id,
            VaccineCreate(vaccine_name="Rabies", administered_at=now),
            test_user,
        )
        assert vaccine is not None
        assert vaccine.vaccine_name == "Rabies"

        vaccines = service.list_vaccines(cat.id, test_user)
        assert len(vaccines) >= 1

        CatService(db).delete_cat(cat.id, test_user)

    def test_create_and_list_vet_visits(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = HealthService(db)

        now = datetime.now(timezone.utc)
        visit = service.create_vet_visit(
            cat.id,
            VetVisitCreate(visit_date=now, reason="Checkup"),
            test_user,
        )
        assert visit is not None
        assert visit.reason == "Checkup"

        visits = service.list_vet_visits(cat.id, test_user)
        assert len(visits) >= 1

        CatService(db).delete_cat(cat.id, test_user)
