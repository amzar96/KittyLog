import crud
import logging
from core import models, schemas
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app = FastAPI(
    title="KittyLog",
    description="API for KittyLog",
    version="0.0.1",
    docs_url="/docs",
)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
