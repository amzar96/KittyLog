from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings

connect_args = {}
if settings.SUPABASE_DB_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.SUPABASE_DB_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
