import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.domains.cats.models import Cat
from src.domains.health.models import CatVaccine, CatWeight, DailyHealth, VetVisit
from src.domains.health.schemas import (
    DailyHealthCreate,
    DailyHealthUpdate,
    VaccineCreate,
    VetVisitCreate,
    WeightCreate,
)
from src.shared.models.user import User

logger = logging.getLogger(__name__)


class HealthService:
    def __init__(self, db: Session):
        self.db = db

    def _get_cat(self, cat_id: str, user: User) -> Cat | None:
        return (
            self.db.query(Cat)
            .filter(Cat.id == cat_id, Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .first()
        )

    # Weight tracking
    def list_weights(self, cat_id: str, user: User) -> list[CatWeight]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []
        return (
            self.db.query(CatWeight)
            .filter(CatWeight.cat_id == cat_id, CatWeight.is_deleted == False)  # noqa: E712
            .order_by(CatWeight.recorded_at.desc())
            .all()
        )

    def create_weight(self, cat_id: str, payload: WeightCreate, user: User) -> CatWeight | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        weight = CatWeight(
            weight=payload.weight,
            recorded_at=payload.recorded_at or datetime.now(timezone.utc),
            notes=payload.notes,
            cat_id=cat_id,
        )
        self.db.add(weight)
        self.db.commit()
        self.db.refresh(weight)
        logger.info("weight recorded", extra={"cat_id": cat_id, "weight": payload.weight})
        return weight

    # Vaccine tracking
    def list_vaccines(self, cat_id: str, user: User) -> list[CatVaccine]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []
        return (
            self.db.query(CatVaccine)
            .filter(CatVaccine.cat_id == cat_id, CatVaccine.is_deleted == False)  # noqa: E712
            .order_by(CatVaccine.administered_at.desc())
            .all()
        )

    def create_vaccine(self, cat_id: str, payload: VaccineCreate, user: User) -> CatVaccine | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        vaccine = CatVaccine(
            vaccine_name=payload.vaccine_name,
            administered_at=payload.administered_at,
            next_due_at=payload.next_due_at,
            notes=payload.notes,
            cat_id=cat_id,
        )
        self.db.add(vaccine)
        self.db.commit()
        self.db.refresh(vaccine)
        logger.info("vaccine recorded", extra={"cat_id": cat_id, "vaccine": payload.vaccine_name})
        return vaccine

    # Vet visits
    def list_vet_visits(self, cat_id: str, user: User) -> list[VetVisit]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return []
        return (
            self.db.query(VetVisit)
            .filter(VetVisit.cat_id == cat_id, VetVisit.is_deleted == False)  # noqa: E712
            .order_by(VetVisit.visit_date.desc())
            .all()
        )

    def create_vet_visit(self, cat_id: str, payload: VetVisitCreate, user: User) -> VetVisit | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        visit = VetVisit(
            visit_date=payload.visit_date,
            clinic_name=payload.clinic_name,
            vet_name=payload.vet_name,
            reason=payload.reason,
            notes=payload.notes,
            cat_id=cat_id,
        )
        self.db.add(visit)
        self.db.commit()
        self.db.refresh(visit)
        logger.info("vet visit recorded", extra={"cat_id": cat_id})
        return visit

    # Daily health
    def get_daily_health(self, cat_id: str, log_date: datetime, user: User) -> DailyHealth | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None
        return (
            self.db.query(DailyHealth)
            .filter(
                DailyHealth.cat_id == cat_id,
                DailyHealth.log_date == log_date,
                DailyHealth.is_deleted == False,  # noqa: E712
            )
            .first()
        )

    def create_daily_health(self, cat_id: str, payload: DailyHealthCreate, user: User) -> DailyHealth | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        health = DailyHealth(**payload.model_dump(), cat_id=cat_id)
        self.db.add(health)
        self.db.commit()
        self.db.refresh(health)
        logger.info("daily health logged", extra={"cat_id": cat_id, "date": str(payload.log_date)})
        return health

    def update_daily_health(
        self, cat_id: str, health_id: str, payload: DailyHealthUpdate, user: User
    ) -> DailyHealth | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        health = (
            self.db.query(DailyHealth)
            .filter(DailyHealth.id == health_id, DailyHealth.cat_id == cat_id, DailyHealth.is_deleted == False)  # noqa: E712
            .first()
        )
        if not health:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(health, field, value)

        self.db.commit()
        self.db.refresh(health)
        return health
