from src.domains.auth.service import get_or_create_user, get_user_by_email


class TestAuthService:
    def test_get_user_by_email_found(self, db, test_user):
        result = get_user_by_email(db, test_user.email)
        assert result is not None
        assert result.email == test_user.email

    def test_get_user_by_email_not_found(self, db):
        result = get_user_by_email(db, "nonexistent@example.com")
        assert result is None

    def test_get_or_create_user_existing(self, db, test_user):
        userinfo = {"email": test_user.email, "name": test_user.full_name}
        result = get_or_create_user(db, userinfo)
        assert result.id == test_user.id

    def test_get_or_create_user_new(self, db):
        userinfo = {"email": "newuser@example.com", "name": "New User", "picture": "https://example.com/pic.jpg"}
        result = get_or_create_user(db, userinfo)
        assert result.email == "newuser@example.com"
        assert result.full_name == "New User"
        assert result.picture_url == "https://example.com/pic.jpg"

        # Clean up
        db.delete(result)
        db.commit()
