import logging
from core import models
from config import common
from core.db import get_db

logger = logging.getLogger(__name__)

db = get_db()


def get_user_by_email(email: str):
    query = (
        db.query(models.User)
        .filter(models.User.email == email, models.User.is_deleted == False)
        .first()
    )

    if query:
        logger.info(f"User is found - {query.email}")
        return query
    else:
        return False


def create_user(user: dict):
    full_name = user.name
    email = user.email
    picture_url = user.picture

    try:
        query = models.User(email=email, full_name=full_name)
        logger.info(f"User to be created - {query.email}")
        common.add_record(query)
        
        return query
    except Exception as e:
        logger.error(e)
