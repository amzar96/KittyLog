import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.dependencies import get_current_user
from src.main import app
from src.shared.models.base import Base
from src.shared.models.user import User
from src.utils.db import get_db

# Import all models so Base.metadata knows about them
from src.domains.cats import models as _cats  # noqa: F401
from src.domains.health import models as _health  # noqa: F401
from src.domains.nutrition import models as _nutrition  # noqa: F401
from src.domains.diary import models as _diary  # noqa: F401
from src.domains.monitoring import models as _monitoring  # noqa: F401
from src.domains.appointments import models as _appointments  # noqa: F401
from src.domains.notifications import models as _notifications  # noqa: F401

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def test_user(db):
    user = User(email="test@example.com", full_name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.query(User).filter(User.id == user.id).delete()
    db.commit()


@pytest.fixture
def client(db, test_user):
    def override_get_db():
        yield db

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
