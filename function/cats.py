import logging
from core.db import get_db
from core import models, schemas
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
tags = ["cats"]
router = APIRouter(tags=tags)

db = get_db()


@router.get("/cats/{name}", response_model=schemas.CatBase)
async def get_cat(name: str):
    query = db.query(models.Cat).filter(models.Cat.name == name).first()

    if query:
        return query
    else:
        raise HTTPException(status_code=404, detail="Data not found")


@router.post("/cats/", response_model=schemas.CatBase)
async def create_cat(cat: schemas.CatCreate):
    user_query = (
        db.query(models.User).filter(models.User.email == cat.owner_email).first()
    )

    query = (
        db.query(models.Cat)
        .filter(models.Cat.name == cat.name)
        .filter(models.Cat.owner == user_query)
        .first()
    )
    if query:
        raise HTTPException(
            status_code=400,
            detail=f"Cat ({cat.name}) already registered under ({cat.owner_email})",
        )

    user = db.query(models.User).filter(models.User.email == cat.owner_email).first()
    query = models.Cat(name=cat.name, nickname=cat.nickname, owner=user)

    db.add(query)
    db.commit()
    db.refresh(query)

    return query
