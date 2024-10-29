import logging
from config import common
from core.db import get_db
from function import users
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


def get_cats_by_owner_email(email: str):
    user = users.get_user_by_email(email)
    query = db.query(models.Cat).filter(models.Cat.owner == user).all()

    if query:
        logger.info(f"Owner cat is found")
        return query
    else:
        return False


def create_cat(name: str, nickname: str, user: models.User):
    query = (
        db.query(models.Cat)
        .filter(models.Cat.name == name)
        .filter(models.Cat.owner == user)
        .first()
    )

    if query:
        raise Exception(f"Cat ({name}) already registered under ({user.email})")

    try:
        query = models.Cat(name=name, nickname=nickname, owner_id=user.id)
        common.add_record(query)

        return query
    except Exception as e:
        logger.error(e)
