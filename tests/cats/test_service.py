import pytest

from src.domains.cats.schemas import CatCreate, CatUpdate
from src.domains.cats.service import CatService


class TestCatService:
    def test_create_cat(self, db, test_user):
        service = CatService(db)
        payload = CatCreate(name="Luna", nickname="lulu")
        cat = service.create_cat(payload, test_user)

        assert cat.name == "Luna"
        assert cat.nickname == "lulu"
        assert cat.owner_id == test_user.id

        # Clean up
        service.delete_cat(cat.id, test_user)

    def test_create_duplicate_cat_raises(self, db, test_user):
        service = CatService(db)
        payload = CatCreate(name="Mochi", nickname="momo")
        cat = service.create_cat(payload, test_user)

        with pytest.raises(ValueError, match="already registered"):
            service.create_cat(payload, test_user)

        service.delete_cat(cat.id, test_user)

    def test_get_cats_by_owner(self, db, test_user):
        service = CatService(db)
        cat1 = service.create_cat(CatCreate(name="Alpha", nickname="a"), test_user)
        cat2 = service.create_cat(CatCreate(name="Beta", nickname="b"), test_user)

        cats = service.get_cats_by_owner(test_user)
        assert len(cats) >= 2

        service.delete_cat(cat1.id, test_user)
        service.delete_cat(cat2.id, test_user)

    def test_get_cat_by_id(self, db, test_user):
        service = CatService(db)
        cat = service.create_cat(CatCreate(name="Neko", nickname="nk"), test_user)

        found = service.get_cat_by_id(cat.id, test_user)
        assert found is not None
        assert found.name == "Neko"

        service.delete_cat(cat.id, test_user)

    def test_update_cat(self, db, test_user):
        service = CatService(db)
        cat = service.create_cat(CatCreate(name="Kitty", nickname="kt"), test_user)

        updated = service.update_cat(cat.id, CatUpdate(nickname="kitkat"), test_user)
        assert updated.nickname == "kitkat"

        service.delete_cat(cat.id, test_user)

    def test_delete_cat_soft_deletes(self, db, test_user):
        service = CatService(db)
        cat = service.create_cat(CatCreate(name="Ghost", nickname="gh"), test_user)

        result = service.delete_cat(cat.id, test_user)
        assert result is True

        found = service.get_cat_by_id(cat.id, test_user)
        assert found is None

    def test_cannot_access_other_users_cat(self, db, test_user):
        from src.shared.models.user import User

        other_user = User(email="other@example.com", full_name="Other")
        db.add(other_user)
        db.commit()
        db.refresh(other_user)

        service = CatService(db)
        cat = service.create_cat(CatCreate(name="Private", nickname="prv"), test_user)

        found = service.get_cat_by_id(cat.id, other_user)
        assert found is None

        deleted = service.delete_cat(cat.id, other_user)
        assert deleted is False

        # Clean up
        service.delete_cat(cat.id, test_user)
        db.delete(other_user)
        db.commit()
