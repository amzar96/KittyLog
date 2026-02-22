from datetime import datetime, timezone

from src.domains.cats.schemas import CatCreate
from src.domains.cats.service import CatService
from src.domains.diary.schemas import DiaryEntryCreate, DiaryEntryUpdate
from src.domains.diary.service import DiaryService


class TestDiaryService:
    def _create_cat(self, db, user):
        service = CatService(db)
        return service.create_cat(CatCreate(name="DiaryCat", nickname="dc"), user)

    def test_create_and_list_entries(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = DiaryService(db)

        entry = service.create_entry(
            cat.id,
            DiaryEntryCreate(entry_date=datetime.now(timezone.utc), content="Had a great day!"),
            test_user,
        )
        assert entry is not None
        assert entry.content == "Had a great day!"

        entries, total = service.list_entries(cat.id, test_user)
        assert total >= 1

        CatService(db).delete_cat(cat.id, test_user)

    def test_update_entry(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = DiaryService(db)

        entry = service.create_entry(
            cat.id,
            DiaryEntryCreate(entry_date=datetime.now(timezone.utc), content="Original"),
            test_user,
        )

        updated = service.update_entry(cat.id, entry.id, DiaryEntryUpdate(content="Updated"), test_user)
        assert updated.content == "Updated"

        CatService(db).delete_cat(cat.id, test_user)

    def test_delete_entry(self, db, test_user):
        cat = self._create_cat(db, test_user)
        service = DiaryService(db)

        entry = service.create_entry(
            cat.id,
            DiaryEntryCreate(entry_date=datetime.now(timezone.utc), content="To delete"),
            test_user,
        )

        result = service.delete_entry(cat.id, entry.id, test_user)
        assert result is True

        found = service.get_entry(cat.id, entry.id, test_user)
        assert found is None

        CatService(db).delete_cat(cat.id, test_user)
