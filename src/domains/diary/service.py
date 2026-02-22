import logging

from sqlalchemy.orm import Session

from src.domains.cats.models import Cat
from src.domains.diary.models import DiaryEntry
from src.domains.diary.schemas import DiaryEntryCreate, DiaryEntryUpdate
from src.shared.models.user import User

logger = logging.getLogger(__name__)


class DiaryService:
    def __init__(self, db: Session):
        self.db = db

    def _get_cat(self, cat_id: str, user: User) -> Cat | None:
        return (
            self.db.query(Cat)
            .filter(Cat.id == cat_id, Cat.owner_id == user.id, Cat.is_deleted == False)  # noqa: E712
            .first()
        )

    def list_entries(self, cat_id: str, user: User, page: int = 1, page_size: int = 20) -> tuple[list[DiaryEntry], int]:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return [], 0

        query = (
            self.db.query(DiaryEntry)
            .filter(DiaryEntry.cat_id == cat_id, DiaryEntry.is_deleted == False)  # noqa: E712
            .order_by(DiaryEntry.entry_date.desc())
        )
        total = query.count()
        entries = query.offset((page - 1) * page_size).limit(page_size).all()
        return entries, total

    def get_entry(self, cat_id: str, entry_id: str, user: User) -> DiaryEntry | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None
        return (
            self.db.query(DiaryEntry)
            .filter(DiaryEntry.id == entry_id, DiaryEntry.cat_id == cat_id, DiaryEntry.is_deleted == False)  # noqa: E712
            .first()
        )

    def create_entry(self, cat_id: str, payload: DiaryEntryCreate, user: User) -> DiaryEntry | None:
        cat = self._get_cat(cat_id, user)
        if not cat:
            return None

        entry = DiaryEntry(**payload.model_dump(), cat_id=cat_id)
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        logger.info("diary entry created", extra={"cat_id": cat_id})
        return entry

    def update_entry(self, cat_id: str, entry_id: str, payload: DiaryEntryUpdate, user: User) -> DiaryEntry | None:
        entry = self.get_entry(cat_id, entry_id, user)
        if not entry:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(entry, field, value)

        self.db.commit()
        self.db.refresh(entry)
        return entry

    def delete_entry(self, cat_id: str, entry_id: str, user: User) -> bool:
        entry = self.get_entry(cat_id, entry_id, user)
        if not entry:
            return False

        entry.is_deleted = True
        self.db.commit()
        return True
