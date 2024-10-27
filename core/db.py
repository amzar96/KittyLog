from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import cfg as CFG

SQLALCHEMY_DATABASE_URL = CFG.SQLITE_DB_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
