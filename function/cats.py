import logging
from config import common
from core.db import get_db
from core import models, schemas
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

db = get_db()


def get_cat_by_nickname(nickname: str, user: models.User):
    query = (
        db.query(models.Cat)
        .filter(models.Cat.nickname == nickname, models.Cat.owner == user)
        .first()
    )

    if query:
        logger.info(f"Cat is found - {query.nickname} {query.owner}")
        return query
    else:
        return False


def create_cat(name: str, nickname: str, user: models.User):
    email = user.email

    user_query = db.query(models.User).filter(models.User.email == email).first()

    query = (
        db.query(models.Cat)
        .filter(models.Cat.name == name)
        .filter(models.Cat.owner == user_query)
        .first()
    )

    if query:
        raise HTTPException(
            status_code=400,
            detail=f"Cat ({name}) already registered under ({email})",
        )

    try:
        query = models.Cat(name=name, nickname=nickname, owner=user_query)
        common.add_record(query)
        return query
    except Exception as e:
        logger.error(e)
