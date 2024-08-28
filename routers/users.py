import logging
from database.db import get_db
from core import models, schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
tags = ["users"]
router = APIRouter(tags=tags)

db = get_db()


def get_user_by_username(username: str):
    return db.query(models.User).filter(models.User.username == username).first()


@router.get("/users/{username}", response_model=schemas.UserBase)
async def get_user(username: str):
    logger.info(username)
    return get_user_by_username(username=username)


@router.post("/users/", response_model=schemas.UserBase)
async def create_user(user: schemas.UserCreate):
    db_user = get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    logger.info(user.email)
    query = models.User(email=user.email, username=user.username)
    logger.info(query)

    db.add(query)
    db.commit()
    db.refresh(query)

    return query
