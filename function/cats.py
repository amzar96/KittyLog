import logging
from config import common
from core.db import get_db
from function import users
from datetime import datetime
from core import models, schemas
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

db = get_db()


def get_cat_by_nickname_name(value: str, _type: str, user: models.User):
    query = db.query(models.Cat)

    if _type == "nickname":
        query = query.filter(models.Cat.nickname == value, models.Cat.owner == user)
    if _type == "name":
        query = query.filter(models.Cat.name == value, models.Cat.owner == user)

    query = query.first()

    if query:
        logger.info(f"Cat is found - {query.nickname} {query.owner}")
        return query
    else:
        return False


def get_cats_by_owner_email(email: str):
    user = users.get_user_by_email(email)

    if user:
        query = (
            db.query(models.Cat)
            .filter(models.Cat.owner == user)
            .filter(models.Cat.is_deleted == False)
            .order_by(models.Cat.name)
            .all()
        )
    else:
        return False

    if query:
        logger.info(f"Owner cat is found")
        return query
    else:
        return False


def create_cat(name: str, nickname: str, dob_date, user: models.User):
    query = (
        db.query(models.Cat)
        .filter(models.Cat.name == name)
        .filter(models.Cat.owner == user)
        .first()
    )

    if query:
        raise Exception(f"Cat ({name}) already registered under ({user.email})")

    try:
        query = models.Cat(name=name, nickname=nickname, dob=dob_date, owner_id=user.id)

        db.add(query)
        db.commit()
        db.refresh(query)

        logger.info(query)

        return query
    except Exception as e:
        logger.error(e)


def update_cat(payload: schemas.CatUpdate, user: models.User):
    try:
        cat = get_cat_by_nickname_name(value=payload.name, _type="name", user=user)

        if not cat:
            raise Exception(f"Cat ({payload.name}) not exist")

        query = (
            db.query(models.Cat)
            .filter(models.Cat.id == cat.id)
            .update(payload.model_dump(exclude_unset=True), synchronize_session=False)
        )

        db.commit()
        db.refresh(cat)

        return query
    except Exception as e:
        logger.error(e)
