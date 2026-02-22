import logging

from sqlalchemy.orm import Session

from src.domains.cats.models import Cat
from src.domains.cats.schemas import CatCreate, CatUpdate
from src.shared.models.user import User

logger = logging.getLogger(__name__)


class CatService:
    def __init__(self, db: Session):
        self.db = db

    def get_cats_by_owner(self, user: User) -> list[Cat]:
        return (
            self.db.query(Cat)
            .filter(Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .order_by(Cat.name)
            .all()
        )

    def get_cat_by_id(self, cat_id: str, user: User) -> Cat | None:
        return (
            self.db.query(Cat)
            .filter(Cat.id == cat_id, Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .first()
        )

    def create_cat(self, payload: CatCreate, user: User) -> Cat:
        existing = (
            self.db.query(Cat)
            .filter(Cat.name == payload.name, Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .first()
        )
        if existing:
            raise ValueError(f"Cat named '{payload.name}' already registered")

        cat = Cat(**payload.model_dump(), owner_id=user.id)
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        logger.info("cat created", extra={"cat_id": cat.id, "user_id": user.id})
        return cat

    def update_cat(self, cat_id: str, payload: CatUpdate, user: User) -> Cat | None:
        cat = self.get_cat_by_id(cat_id, user)
        if not cat:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(cat, field, value)

        self.db.commit()
        self.db.refresh(cat)
        return cat

    def delete_cat(self, cat_id: str, user: User) -> bool:
        cat = self.get_cat_by_id(cat_id, user)
        if not cat:
            return False

        cat.is_deleted = True
        self.db.commit()
        return True
